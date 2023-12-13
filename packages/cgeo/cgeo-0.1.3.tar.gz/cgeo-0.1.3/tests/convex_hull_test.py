import json
import os

from cgeo.modules.polygon import Point
from cgeo.utilities.c_utilities.global_c_utils import grahamConvexHull
from tests.process_json_files import extractJsonFiles
from tests.shapes2d.polygoon_test import testValidPolygon, testForConvexPolygon

def testRun():
    directory_path = os.path.join(os.path.dirname(__file__), 'inputs', 'convex_hull')
    inputFiles = extractJsonFiles(directory_path)

    for _input in inputFiles:
        with open(_input, 'r') as f:
            try:
                data = json.load(f)

                points = [Point(point["x"], point["y"]) for point in data["points"]]
                convexPoly = grahamConvexHull(points)

                assert testValidPolygon(convexPoly) and testForConvexPolygon(convexPoly)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {_input}: {e}")
            except Exception as e:
                print(f"Error processing {_input}: {e}")

            return True
