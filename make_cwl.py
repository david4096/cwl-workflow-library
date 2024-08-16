import os
import pandas as pd
import numpy as np


def create_placeholder_file(directory, label):
    """Creates an empty file in the specified directory with the name based on the label."""
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
    file_name = f"{label.replace(' ', '_').replace('/', '_')}.cwl"
    file_path = os.path.join(directory, file_name)
    open(file_path, 'a').close()  # Touch the file


def format_authors(authors):
    """Formats the authors list, handling comma-separated values."""

    return [{'name': authors}]


def create_dockstore_yml(df, output_dir):
    """Creates the .dockstore.yml file with tools or workflows sections based on class."""
    dockstore_content = "version: 1.2\n"

    tools_section = "tools:\n"
    workflows_section = "workflows:\n"

    for _, row in df.iterrows():
        try:
            # Replace spaces and slashes in label with underscores
            directory_name = row['label'].replace(' ', '_').replace('/', '_')
            create_placeholder_file(os.path.join(output_dir, directory_name), directory_name)

            # Create the Dockstore entry
            authors = format_authors(row.get('sbg:toolAuthor', ''))
            wrapper_author = row.get('sbg:wrapperAuthor', None)
            if wrapper_author and wrapper_author not in [author['name'] for author in authors]:
                authors.append({'name': wrapper_author})

            entry_content = "  - subclass: CWL\n"
            entry_content += f"    primaryDescriptorPath: ./{output_dir}/{directory_name}/{directory_name}.cwl\n"

            if authors:
                entry_content += "    authors:\n"
                for author in authors:
                    entry_content += f"      - name: {author['name']}\n"

            topic = row.get('sbg:categories', None)
            if topic:
                entry_content += f"    topic: {topic}\n"

            if row['class'] == 'CommandLineTool':
                tools_section += entry_content
            elif row['class'] == 'Workflow':
                workflows_section += entry_content

        except Exception as e:
            print(f"Failed to process row with label '{row['label']}': {e}")

    if "CommandLineTool" in df['class'].values:
        dockstore_content += tools_section
    if "Workflow" in df['class'].values:
        dockstore_content += workflows_section

    with open('.dockstore.yml', 'w') as f:
        f.write(dockstore_content)


def main():
    # Configuration
    output_dir = 'my_workflows'  # Set your desired output directory here

    # Load the DataFrame from the CSV file
    df = pd.read_csv('cwl_dataframe.csv')

    # Replace 'nan' with np.nan for consistent handling
    df.replace('nan', np.nan, inplace=True)

    # Create placeholder files and the .dockstore.yml file
    create_dockstore_yml(df, output_dir)

    print("Placeholder files and .dockstore.yml have been created successfully.")


if __name__ == "__main__":
    main()
