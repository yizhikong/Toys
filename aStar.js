function Node(point, p, h, prePoint) {
	this.point = point;
	this.p = p; // current cost
	this.h = h; // guess cost
	this.f = p + h; // all cost
	this.pre = prePoint; // pre point
	this.equal = function(obj) {
		if (this.point.equal(obj.point)) {
			return true;
		} else {
			return false;
		}
	}
}
function Point(x, y) {
	this.x = x;
	this.y = y;
	this.equal = function(obj) {
		if (this.x == obj.x && this.y == obj.y) {
			return true;
		} else {
			return false;
		}
	}
}
function getH(sp, tp) {
	return Math.sqrt((sp.x-tp.x)*(sp.x-tp.x) + (sp.y-tp.y)*(sp.y-tp.y));
}
// function selectPoint choose the most possible point
function selectPoint(openList) {
	len = openList.length;
	minPos = len - 1;
	minCost = openList[len - 1].f;
	for (i = len-1; i >= 0; i--) {
		if (openList[i].f < minCost) {
			minPos = i;
			minCost = openList[i].f;
		}
	}
	return minPos;
}
function getMessage(minNode) {
    /*
		use database here.
		return a list containing the nodes which the minNode can get.
		remenber to set the p, h and f before push the node into the nodeList!
	*/
	return nodeList;
}
function pStr(point) {
	return "(" + point.x + ", " + point.y + ")";
}
function find(sx, sy, tx, ty) {
	var openList = new Array();
	var closeList = new Array();
	var prePoint = new Array();
	var pointStatus = new Array();
	var sp = new Point(sx, sy);
	var tp = new Point(tx, ty);
	var sn = new Node(sp, 0, getH(sp, tp), sp);
	var tn = new Node(tp, 0, 0, tp);
	openList.push(sn);
	pointStatus[pStr(sp)] = 1;
	prePoint[pStr(sp)] = pStr(sp);
	while (openList.length > 0) {
		// choose the most possible point
		minPos = selectPoint(openList);
		minNode = openList[minPos];
		// move the point from openList to closeList
		openList.splice(minPos, 1);
		openList.length
		closeList.push(minNode);
		pointStatus[pStr(minNode.point)] = -1;
		prePoint[pStr(minNode.point)] = pStr(minNode.pre);
		// judge if have ended
		if (tp.equal(minNode.point)) {
			
			break;
		}
		// add points
		var reachableList = new Array();
		reachableList = getMessage(minNode);
		for (i = 0; i < reachableList.length; i++) {
			currentStr = pStr(reachableList[i].point);
			status = pointStatus[currentStr];
			// point has been in closeList
			if (status == -1) {
				continue;
			}
			// new point
			if (status == undefined) {
				reachableList[i].h = getH(reachableList[i].point, tp);
				reachableList[i].f = reachableList[i].p + reachableList[i].h;
				reachableList[i].pre = minNode.point;
				openList.push(reachableList[i]);
				pointStatus[currentStr] = 1;
			} else {
				// point has been in openList, fresh the point
				// p means current cost, h means guess cost, f means all cost
				var j;
				var pos = 0;
				for (j = 0; j < openList.length; j++) {
				    if (openList[j].equal(reachableList[i])) {
					    pos = j;
						break;
					}
				}
				originF = openList[pos].f;
				newF = reachableList[i].f;
				if (newF < originF) {
					openList[pos].pre = minNode.point;
					openList[pos].p = reachableList[i].p;
					openList[pos].f = newF;
				}
			}
		}
	}
	ret = ""; // the string of path, from target point to source point
	sStr = pStr(sp);
	printStr = pStr(tp);
	while (printStr != sStr) {
		console.log(printStr);
		ret = ret + printStr + "\n";
		printStr = prePoint[printStr];
	}
	console.log(printStr);
	return ret;
}

//example : find(2, 4, 20, 6). Source point(2, 4), target point(20, 6)
exports.find = find;
