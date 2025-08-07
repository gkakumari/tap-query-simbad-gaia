import pandas as pd
from tqdm import tqdm
from astropy.table import Table
import pyvo as vo


# Initialize SIMBAD TAP service
simbadtap = vo.dal.TAPService("http://simbad.u-strasbg.fr/simbad/sim-tap")


def pprint_columns_description(tablename, service=simbadtap):
    """
    Pretty-print column names, types, and descriptions for a given TAP table.
    """
    rows = []
    query = f"SELECT TOP 0 * FROM {tablename}"
    table = service.run_sync(query).to_table()
    for col in table.itercols():
        rows.append([col.name, col.dtype.str, col.description])
    return Table(rows=rows, names=["colname", "dtype", "description"])


def custom_agg(x):
    """
    Aggregation function:
    - Return value if all values in a group are the same
    - Else return a list of values
    """
    return x.iloc[0] if len(set(x)) == 1 else x.tolist()


def load_target_list(filename):
    """
    Load a whitespace-delimited file containing Gaia source IDs.
    """
    return pd.read_csv(filename, sep='\s+')


def list_available_tables(service=simbadtap):
    """
    List available user-defined tables from the SIMBAD TAP service.
    """
    query = """
        SELECT * FROM TAP_SCHEMA.tables 
        WHERE schema_name NOT LIKE 'TAP_SCHEMA'
    """
    result = service.run_sync(query).to_table()
    print(f"Number of available tables: {len(result)}")
    return result['table_name', 'description']


def query_simbad_for_sources(service=simbadtap, source_ids=None, id_prefix="Gaia DR3"):
    """
    Query SIMBAD TAP for a list of Gaia DR3 source IDs.
    """
    all_results = []

    for sid in tqdm(source_ids, desc="Querying SIMBAD"):
        full_id = f"{id_prefix}{sid}"

        query = f"""
        SELECT
            b.main_id,
            b.otype,
            b.otype_txt,
            i.id AS gaia_id,
            ot.label AS other_type,
            mesSpT.oidref AS spt_oid,
            mesSpT.sptype,
            mesSpT.bibcode AS spt_bibcode,
            mesFe_H.log_g,
            mesFe_H.teff,
            mesFe_H.bibcode AS feh_bibcode,
            mesFe_H.oidref AS feh_oid
        FROM basic AS b
        JOIN ident AS i ON b.oid = i.oidref
        JOIN otypedef AS ot ON b.otype = ot.otype
        LEFT JOIN mesSpT USING(oidref)
        LEFT JOIN mesFe_H USING(oidref)
        WHERE id = '{full_id}'
        ORDER BY id
        """

        try:
            result = service.run_sync(query)
            df = result.to_table().to_pandas()
            all_results.append(df)
        except Exception as e:
            print(f"Query failed for source_id {sid}: {e}")

    if all_results:
        return pd.concat(all_results, ignore_index=True)
    else:
        return pd.DataFrame()


def id_exists_in_simbad(service, full_id):
    """
    Check if a Gaia DR3 ID exists in SIMBAD's 'ident' table.

    Parameters:
        service (pyvo.dal.TAPService): The TAP service.
        full_id (str): The full SIMBAD ID, e.g., 'Gaia DR3<source_id>'.

    Returns:
        bool: True if the ID exists in SIMBAD, False otherwise.
    """
    query = f"SELECT TOP 1 id FROM ident WHERE id = '{full_id}'"
    try:
        result = service.run_sync(query)
        return len(result.to_table()) > 0
    except Exception:
        return False
    
def reorder_columns(df, first_col_name):
    """
    Move a specified column to the front.
    """
    first_col = df[first_col_name]
    df = df.drop(columns=[first_col_name])
    return pd.concat([first_col, df], axis=1)


def group_by_id(df, id_column="gaia_id"):
    """
    Group by Gaia ID and aggregate duplicated entries.
    """
    return df.groupby(id_column).agg(custom_agg).reset_index()
