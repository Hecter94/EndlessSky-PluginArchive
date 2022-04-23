//The code below is from souce/ship.cpp
//Use caution when editing souce code...

//I would like fat heavy ships to fly like an oil tanker, so this code change
//would reduce felt hit force from weapons fire.

//The bulk of this data is so you can find it in the file.


// Apply a force to this ship, accelerating it. This might be from a weapon
// impact, or from firing a weapon, for example.
void Ship::ApplyForce(const Point &force, bool gravitational)
{
	if(gravitational)
	{
		// Treat all ships as if they have a mass of 400. This prevents
		// gravitational hit force values from needing to be extremely
		// small in order to have a reasonable effect.
		acceleration += force / 400.;
		return;
	}
	
	double currentMass = Mass();
	if(!currentMass)
		return;
	
	// Reduce acceleration of small ships and increase acceleration of large
	// ones by having 30% of the force be based on a fixed mass of 400, i.e. the
	// mass of a typical light warship:
	acceleration += force * (.3 / 400. + .7 / currentMass);
}

//Change	
	"acceleration += force * (.3 / 400. + .7 / currentMass);"
//to		
	"acceleration += force / currentMass * 0.8;"


