from rover_lib import location, relative_heading

class ObjectRegistry:

	def __init__(self):
		self.registry = []

	def add(self, point):
		self.registry.append(point)

	def determine_safe_heading(self, desired, rover_loc):
		des = int(desired)
		safe_heading = range(0,360)
		for obj in self.registry:
			heading = math.atan2((obj[1] - rover_loc[1]), (obj[0] - rover_loc[0])) * 180 / math.pi
			dist = math.sqrt( (obj[0] - rover_loc[0])**2 + (obj[1] - rover_loc[1])**2)
			radius = gain * dist

			bound_l = int(heading - radius)
			bound_u = int(heading + radius)

			bounded = list(range(bound_l, bound_u))
			safe_headings = [item for item in safe_heading if item not in bounded]
			safe_heading = safe_headings
			
		best_hdg = des+180
		for hdg in safe_heading:
			if abs(des - hdg) < abs(des - best_hdg):
				best_hdg = hdg

		return best_hdg

	def purge(rover_loc, waypoint):
		# call every step
		waypoint_vec = [waypoint[0]-rover_loc[0], 
						waypoint[1]-rover_loc[1], waypoint[2]-rover_loc[2]]
		for i in range(len(self.registry)):
			obj = self.registry[i]
			if obj[0] - waypoint[0] < 0 and obj[1] - waypoint[1] < 0:
				self.registry.pop(i)


