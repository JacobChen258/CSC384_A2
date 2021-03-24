#!/bin/bash

# dir=$(dirname "$(readlink -f "$0")") # ubuntu
dir=$(dirname "$(greadlink -f "$0")") # mac

# Making sure a parameter is passed in.
if [ -z $1 ]; then
	echo "you need to pass a utorid/groupid as the parameter."
	exit 1
fi

student="$1"

# Checking to see if the utorid/groupid directory exists in the handed in assignments.
if [ ! -d "${dir}/student_solutions/$student" ]; then
	echo "student utorid does not exist."
	exit 1
fi


# Deleting old text file.
echo "deleted old mark."
rm -f "${dir}/student_marks/$student-autograder-mark.txt"

echo "Marking \"$student\""

echo "Making independent environment."
mkdir -p "${dir}/student_solution_envs/${student}-student-marking-env"
cp -r "${dir}/a2_starter/"* "${dir}/student_solution_envs/${student}-student-marking-env/"

# Deleting Original Files From Environment
rm -f "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/evaluation_functions.py"
rm -f "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/game_tree_searching.py"

# game_tree_searching testing
echo "Running tests on \"game_tree_searching.py\"."
if [ -e "${dir}/student_solutions/${student}/game_tree_searching.py" ];then
	cp -r "${dir}/student_solutions/${student}/game_tree_searching.py" "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/"
else
	cp -r "${dir}/blanks/game_tree_searching.py" "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/"
fi

cp -r "${dir}/perfects/evaluation_functions.py" "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/"

cd "${dir}/student_solution_envs/${student}-student-marking-env/"
date
gts_output=$(timeout 240 python3 "autograder_gts.py" -w 0.0001 2>&1)
cd "${dir}"
gts_mark=$(echo "${gts_output}" | grep "Total Grade - GTS:" | cut -d " " -f5)
gts_output=$(echo "${gts_output}" | grep -v "Total Grade - GTS:")



# evaluation_functions testing
echo "Running tests on \"evaluation_functions.py\"."
if [ -e "${dir}/student_solutions/${student}/evaluation_functions.py" ];then
	cp -r "${dir}/student_solutions/${student}/evaluation_functions.py" "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/"
else
	cp -r "${dir}/blanks/evaluation_functions.py" "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/"
fi

cp "${dir}/perfects/game_tree_searching.py" "${dir}/student_solution_envs/${student}-student-marking-env/game_trees/"

cd "${dir}/student_solution_envs/${student}-student-marking-env/"
date
ef_output=$(timeout 120 python3 "autograder_ef.py" -w 0.0001 2>&1)
cd "${dir}"
ef_mark=$(echo "${ef_output}" | grep "Total Grade - EF:" | cut -d " " -f5 )
ef_output=$(echo "${ef_output}" | grep -v "Total Grade - EF:")



# Final Mark Calculations
numerator=$(echo "$(echo ${gts_mark} | cut -d"/" -f1) + $(echo ${ef_mark} | cut -d"/" -f1)" | bc)
denominator=$(echo "$(echo ${gts_mark} | cut -d"/" -f2) + $(echo ${ef_mark} | cut -d"/" -f2)" | bc)
total_mark="Total Grade: ${numerator}/${denominator}"

echo "Documenting student mark."
echo -e "${gts_output}\n${ef_output}\n\n${total_mark}" > "${dir}/student_marks/${student}-autograder-mark.txt"

rm -rf 	"${dir}/student_solution_envs/${student}-student-marking-env"
echo "Marking Done."


rm -rf "${dir}/student_solution_envs"
