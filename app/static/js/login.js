// Toggles view for officer skills areatext
function toggle_officer_skills() {
var x = document.getElementById("position")
	if (x.value === "PI") {
	  document.getElementById("officer_skills").classList.add("hidden");
	} else {
	  document.getElementById("officer_skills").classList.remove("hidden");
	}
}
