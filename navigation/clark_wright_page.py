import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from algorithms.clark_wright import clark_wright

# ------- Clark_wright_page -------
def clark_wright_page():
    st.title("Clark-Wright Savings Algorithm")
    st.markdown("##### This app helps optimize delivery routes using the Clark-Wright Savings Algorithm.")

    def create_template(max_nodes=20):
        """
        Create a CSV template for user input with a maximum number of nodes.
        Includes a Demand column at the end and a distance matrix.
        """
        nodes = [f'Node {i}' for i in range(1, max_nodes + 1)] + ['Depot']
        data = {node: [np.nan] * len(nodes) for node in nodes}
        template_df = pd.DataFrame(data, index=nodes)
        template_df.index.name = 'Distance'
        np.fill_diagonal(template_df.values, 0)  # Set diagonal to 0 (self-distances)
        
        # Add Demand column at the end
        template_df['Demand'] = [10] * max_nodes + [0]  # Example demands
        return template_df

    def transform_to_complete_matrix(df):
        """
        Transform the uploaded matrix into a complete symmetric matrix.
        """
        # Extract the demand column and remove it from the distance matrix
        demands = df.iloc[:,-1].tolist()

        # Drop columns with missing or unnamed headers
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]
        df = df.loc[:, ~df.columns.isnull()]
        
        distance_matrix = df.iloc[:, :-1]
        
        # Fill missing values symmetrically
        for i in range(len(distance_matrix)):
            for j in range(len(distance_matrix)):
                if pd.isna(distance_matrix.iloc[i, j]):
                    distance_matrix.iloc[i, j] = distance_matrix.iloc[j, i]
                elif pd.isna(distance_matrix.iloc[j, i]):
                    distance_matrix.iloc[j, i] = distance_matrix.iloc[i, j]
        
        return distance_matrix, demands

    def display_matrix_with_dashes(matrix):
        """
        Replace NaN or None values with '--' for display purposes.
        """
        display_matrix = matrix.copy()
        return display_matrix.fillna('--')
    
    def calculate_route_distance(route_nodes, distance_matrix):
        """
        Calculate the total distance for a given route.
        """
        depot_row = -1  # Assuming 'Depot' is the last row
        depot_col = -2  # Assuming 'Depot' is the second-to-last column

        return (
            distance_matrix.iloc[depot_row, distance_matrix.columns.get_loc(route_nodes[0])]  # Depot to first node
            + sum(
                distance_matrix.iloc[
                    distance_matrix.index.get_loc(route_nodes[j]),
                    distance_matrix.columns.get_loc(route_nodes[j + 1])
                ]
                for j in range(len(route_nodes) - 1)  # Between nodes in the route
            )
            + distance_matrix.iloc[
                distance_matrix.index.get_loc(route_nodes[-1]), depot_col
            ]  # Last node to Depot
        )

    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload your populated CSV file*", type=["csv"])

    # Provide template download
    template_df = create_template(max_nodes=20)
    csv_template = BytesIO()
    template_df.to_csv(csv_template)
    csv_template.seek(0)
    
    # Download csv template
    st.sidebar.markdown(
        """
        *Use this template provided.\\
            You may rename the headers, but ensure the order matches the template.
        """
    )

    # Place the download button inside the styled container
    st.sidebar.download_button(
        label="Download 🔻",
        data=csv_template,
        file_name="distance_template.csv",
        mime="text/csv",
    )
    
    if uploaded_file:
        # Load the file into a Pandas DataFrame
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, index_col=0)
        try:
            # Transform the matrix to populate missing values symmetrically
            complete_distance_matrix, demands = transform_to_complete_matrix(df)

            # Add the Demand column back for display purposes
            complete_distance_matrix['Demand'] = demands
            complete_distance_matrix_display = display_matrix_with_dashes(complete_distance_matrix)

            st.subheader("Complete Distance Matrix with Demands")
            st.dataframe(complete_distance_matrix_display)
            
            st.sidebar.markdown("---") 

            # Ask for the maximum capacity
            max_capacity = st.sidebar.number_input("Enter the maximum capacity per tour:", min_value=1, value=50)

            # Perform the Clark-Wright Savings Algorithm
            routes = clark_wright(complete_distance_matrix.iloc[:, :-1], demands, max_capacity)

            # Display results
            st.subheader("Result")
            st.write(f"How many tours needed? {len(routes)}")
            for i, route in enumerate(routes):
                route_nodes = [complete_distance_matrix.index[node] for node in route]
                
                # Calculate total distance for the current route
                total_distance = calculate_route_distance(route_nodes, complete_distance_matrix)
    
                st.write(f"Tour {i + 1}: Depot -> {' -> '.join(route_nodes)} -> Depot. (Total Distance: {total_distance:.2f})")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please upload a populated CSV file from the sidebar to process the results ⚙️")
