from typing import List, Dict
import pandas as pd

def validate_dataframes(df_list: List[pd.DataFrame], check_column_order: bool = False) -> Dict[str, bool]:
    """
    Validate a list of DataFrames to ensure they have consistent structure.

    Args:
        df_list (List[pd.DataFrame]): A list of Pandas DataFrames to validate.
        check_column_order (bool): Whether to check the column order.

    Returns:
        Dict[str, bool]: Dictionary with validation results for:
            - 'same_col_names': whether all DataFrames have the same column names
            - 'same_col_order': whether all DataFrames have the same column order (if check_column_order is True)
            - 'same_dtypes': whether all DataFrames have the same dtypes
    """
    result = {
        "same_col_names": True,
        "same_col_order": True,
        "same_dtypes": True
    }
    
    try:
        if not df_list:
            raise ValueError("Empty list: no DataFrames to validate.")

        ref_df = df_list[0]
        ref_col_set = set(ref_df.columns)
        ref_col_order = list(ref_df.columns)
        ref_dtypes = ref_df.dtypes.astype(str).to_dict()

        for i, df in enumerate(df_list[1:], start=1):
            # Check column names (ignoring order)
            if set(df.columns) != ref_col_set:
                result["same_col_names"] = False

            # Check column order if required
            if check_column_order and list(df.columns) != ref_col_order:
                result["same_col_order"] = False

            # Check dtypes
            current_dtypes = df.dtypes.astype(str).to_dict()
            for col in ref_col_set:
                if col not in current_dtypes or current_dtypes[col] != ref_dtypes[col]:
                    result["same_dtypes"] = False
                    break  # No need to check more columns

        # If not checking column order, remove it from the result
        if not check_column_order:
            result.pop("same_col_order")

        return result

    except Exception as e:
        return {
            "same_col_names": False,
            "same_col_order": False if check_column_order else None,
            "same_dtypes": False,
            "error": str(e)
        }
    