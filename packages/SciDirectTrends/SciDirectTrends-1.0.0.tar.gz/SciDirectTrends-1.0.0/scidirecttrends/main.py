import argparse
import sys
from scidirecttrends import visualization

def main():
    parser = argparse.ArgumentParser(description="SciDirectTrends: Fetch and visualize publication trends from ScienceDirect.")
    parser.add_argument("-t", "--title", required=False, default='Publication Count per Year', type=str, help="The title of the visualization.")
    parser.add_argument("-q", "--query", required=False, default='', type=str, help="The query string to search on ScienceDirect.")
    parser.add_argument("-o", "--output", required=False, default='trend.png', type=str, help="The output filename for the visualization.")

    args = parser.parse_args()

    title = args.title
    query = args.query
    output = args.output

    try:
        visualization.plot_publication_trends(query, output, title)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
