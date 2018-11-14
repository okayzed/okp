mkdir -p compiled/tests

function run_test() {
  name=${1/.cpy/.cpp}
  python src/main.py < ${1} > "compiled/${name}" 
  g++ -x c++ - < "compiled/${name}"
  if [[ $? != 0 ]]; then
    cat -n "compiled/${name}"
    echo "FAILED: ${1}"
  else
    echo "PASSED: ${1}"
  fi

  rm a.out
}


function basic_tests() {
  run_test tests/basic_main.cpy
  run_test tests/basic_class.cpy
  run_test tests/params_test.cpy
  run_test tests/toplevel_invoke.cpy
  run_test tests/nested_identifiers.cpy
  run_test tests/demo_program.cpy
}

function external_tests() {
  run_test tests/quick_print.cpy
  run_test tests/example_class.cpy
  run_test tests/simple_array_max_min.cpy
  run_test tests/scarborough_fair.cpy
  run_test tests/c_look_like_python.cpy
  run_test tests/manacher.cpy
}

basic_tests
external_tests
