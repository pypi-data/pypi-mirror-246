
#include <algorithm>
#include <iostream>
#include "ConvexHull2D.h"

using namespace Algorithms2d;

using Point = Shapes2D::Point2d;
using PointsVector = std::vector<Point>;
using Polygon = Shapes2D::Polygon;



void printStack(const std::stack<Point>& stk) {
    std::stack<Point> tempStk = stk;

    std::cout<<"stack print"<<std::endl;

    while (!tempStk.empty()) {
        std::cout << tempStk.top().toStr() << std::endl;
        tempStk.pop();
    }

    std::cout << std::endl;
}

void printVector(const std::vector<Point>& points) {
    std::cout<< "vector print" << std::endl;

    for (const auto& p : points) {
        std::cout << p.toStr() << std::endl;
    }
}

/**
 * the graham algorithm is an O(nlog(n)) algo. for finding the convex hull of a polygon.
 * the algorithms sorts the points by their x-axis and then eliminate points one by one from being part of the convex.
 * @param poly is a polygon in the plane xy.
 * @return subset of Points picked from the original polygon, which forms the convex hull.
 * @url https://en.wikipedia.org/wiki/Graham_scan
 */
Polygon *ConvexHull::grahamConvexHull(const PointsVector& points) {
    int n = (int)(points.size());

    /* init sorted vector, result and stack for algorithm */
    PointsVector sorted_points = sortByX(points);
    std::stack<Point> stack;
    PointsVector res;

    /* push first two points */
    stack.push(sorted_points[0]);
    stack.push(sorted_points[1]);

    /*
     * in each iter. while stack.size > 2 find valid turn
     * that way we can say the invariant is: in each iter. the stack is full of valid turns
     * */
    for (int i=2; i<n; i++) {
        stack.push(sorted_points[i]);
        while(stack.size()>2 && !right_turn(&stack)) {
            Point tmp = stack.top();
            stack.pop();
            stack.top(); /* very weired .... */
            stack.pop();
            stack.push(tmp);
        }
    }

    /* copy points to res */
    while(!stack.empty()) {
        res.insert(res.begin(), stack.top());
        stack.pop();
    }

    /* do the same for the lower points */
    stack.push(sorted_points[n-1]);
    stack.push(sorted_points[n-2]);
    for (int i=n-3; i>=0; i--) {
        stack.push(sorted_points[i]);
        while(stack.size()>2 && !right_turn(&stack)) {
            Point tmp = stack.top();
            stack.pop();
            stack.top(); /* very weired .... */
            stack.pop();
            stack.push(tmp);
        }
    }

    stack.pop();
    std::stack<Point> reversedStack;
    while(!stack.empty()) {
        reversedStack.push(stack.top());
        stack.pop();
    }
    reversedStack.pop();

    /* copy points to res */
    while(!reversedStack.empty()) {
        res.emplace_back(reversedStack.top());
        reversedStack.pop();
    }

    return new Polygon(res);
}

/**
 * this function responsible for sorting the Points in the Polygon poly. by their x-axis.
 * @param poly Polygon type object
 * @return vector of type Point2d
 */
PointsVector ConvexHull::sortByX(PointsVector points){
    PointsVector res;
    res.assign(points.begin(), points.end());

    std::sort(res.begin(), res.end(), [ ]( const Point & p, const Point& q )
    {
        return p.getX() < q.getX();
    });

    return res;
}

/**
 * this function is responsible for checking if the last three Points in s are performing a right turn.
 * @param s stack of type Point2d
 * @return boolean value
 */
bool ConvexHull::right_turn(std::stack<Point> *s) {
    /* pick three last points */
    Point third = s->top();
    s->pop();
    Point second = s->top();
    s->pop();
    Point first = s->top();
    s->push(second);
    s->push(third);

    /* perform turn checking */
    return first.oriePred(second, third) < 0;
}

/**
 * the algorithm is O(nh) for finding the convex hull of a given polygon, where h is the number of vertices of the output
 * in each step the algorithm finds the next point which is belong to the convex by checking all possibilities.
 * @param poly is a polygon in the plane xy
 * @return subset of Points picked from the original polygon, which forms the convex hull.
 * @url https://en.wikipedia.org/wiki/Gift_wrapping_algorithm
 */
Polygon *ConvexHull::giftWrapConvexHull(PointsVector points) {
    /* init res and point candidate ptr */
    PointsVector res;
    if (points.empty())
        return new Polygon (points);

    auto pointOnHull = points[0];
    for(const auto & point : points)
        if (point < pointOnHull)
            pointOnHull = point;

    Shapes2D::Point2d endPoint;

    /*
     * in every iter we find the next point to be on the hull
     * each iter will take O(n) time
     * overall will make h iterations while h is the number of vertices on the convex hull
     * */
    do {
        res.push_back(pointOnHull);
        endPoint = points[0];
        for (int j=1; j<points.size(); j++){
            if (endPoint == pointOnHull || res.back().oriePred(endPoint, points[j]) > 0) {
                endPoint = points[j];
            }
        }
        pointOnHull = endPoint;
    }while (res[0] != endPoint);

    return new Polygon(res);
}

