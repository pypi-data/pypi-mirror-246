import pandas as pd
if __name__ == "__main__":
    records_clean = pd.read_csv('records_clean.csv')
    
def get_service_counts_by_state(records_clean, state):
    """
    Get the counts of people who received each service for a given state.

    Parameters:
    - records_clean: DataFrame containing the data
    - state: The state for which to get the counts

    Returns:
    - DataFrame with counts for the specified state and each service
    """
    # Filter the DataFrame based on the state
    filtered_df = records_clean[records_clean['State'] == state]

    # Group by 'Indicator(Last 4 Weeks)' and count the number of records for each service
    service_counts = filtered_df.groupby('Indicator(Last 4 Weeks)').size().reset_index(name='Counts')
    # Print a descriptive sentence
    print(f"The number of people who received mental health services in {state} are as follows:")
    print(service_counts)
    return service_counts


def get_service_counts(records_clean, service_indicator):
    """
    Get the counts of people who received a specific service across states.

    Parameters:
    - records_clean: DataFrame containing the data
    - service_indicator: The service indicator to filter ('Took Prescription Medication for Mental Health',
                           'Received Counseling or Therapy',
                           'Took Prescription Medication for Mental Health And/Or Received Counseling or Therapy',
                           'Needed Counseling or Therapy But Did Not Get It')

    Returns:
    - DataFrame with counts for each state and the specified service
    """
    # Filter the DataFrame based on the service indicator
    filtered_df = records_clean[records_clean['Indicator(Last 4 Weeks)'] == service_indicator]

    # Group by 'State' and count the number of records for each state
    service_counts = filtered_df.groupby('State').size().reset_index(name='Count')
    print(f"The numbers of people who {service_indicator.lower()} last 4 weeks in each state are as follows:")
    print(service_counts)
    return service_counts


def display_indicators_for_symptom_presence(records_clean, presence_filter):
    """
    Display counts for four indicators with the specified presence of symptoms of anxiety/depression.

    Parameters:
    - records_clean: DataFrame containing the data
    - presence_filter: The presence filter ("Yes" or "No")

    Returns:
    - DataFrame with counts for each indicator with the specified presence filter
    """
    # Filter the DataFrame based on the presence filter
    filtered_df = records_clean[records_clean['Subgroup'] == presence_filter]

    # Group by 'Indicator(Last 4 Weeks)' and count the number of records for each indicator
    indicator_counts = filtered_df.groupby('Indicator(Last 4 Weeks)').size().reset_index(name='Count')
    print(f"The number of people identified {presence_filter.lower()} for anxiety/depression symptoms who received mental health services are as follows:")
    print(indicator_counts)
    return indicator_counts


def get_service_indicators_by_parameters(records_clean, age=None, sex=None, race=None, education=None, gender_identity=None):
    """
    Get service indicators based on specified query parameters.

    Parameters:
    - records_clean: DataFrame containing the data
    - age: Age subgroup ('18 - 29 years', '30 - 39 years', '40 - 49 years', '50 - 59 years', '60 - 69 years', '70 - 79 years', '80 years and above')
    - sex: Sex subgroup ('Male', 'Female')
    - race: Race subgroup ('Hispanic or Latino', 'Non-Hispanic White, single race', 'Non-Hispanic Black, single race', 'Non-Hispanic Asian, single race', 'Non-Hispanic, other races and multiple races')
    - education: Education subgroup ('Less than a high school diploma', 'High school diploma or GED', 'Some college/Associate's degree', 'Bachelor's degree or higher')
    - gender_identity: Gender identity subgroup ('Cis-gender male', 'Cis-gender female', 'Transgender')

    Returns:
    - DataFrame with service indicators based on the specified query parameters
    """
    # Create a mask based on the specified query parameters
    mask = (
        (records_clean['Group'] == 'By Age') & (records_clean['Subgroup'] == age) if age else True) & \
        ((records_clean['Group'] == 'By Sex') & (records_clean['Subgroup'] == sex) if sex else True) & \
        ((records_clean['Group'] == 'By Race/Hispanic ethnicity') & (records_clean['Subgroup'] == race) if race else True) & \
        ((records_clean['Group'] == 'By Education') & (records_clean['Subgroup'] == education) if education else True) & \
        ((records_clean['Group'] == 'By Gender identity') & (records_clean['Subgroup'] == gender_identity) if gender_identity else True)

    # Apply the mask and filter the DataFrame
    filtered_df = records_clean[mask]

    # Extract relevant columns (adjust as needed)
    selected_columns = ["Indicator(Last 4 Weeks)", "State", "Subgroup", "Group", "Year"]
    result_df = filtered_df[selected_columns]

    return result_df