function run_test() {
  python src/main.py < ${1} | g++ -x c++ -
  if [[ $? != 0 ]]; then
    python src/main.py < ${1} | cat -n
    echo "FAILED: ${1}"
  else
    echo "PASSED: ${1}"
  fi

  rm a.out
}

run_test tests/basic_main.cpy
run_test tests/basic_class.cpy
run_test tests/demo_program.cpy
run_test tests/quick_print.cpy
run_test tests/example_class.cpy
run_test tests/simple_array_max_min.cpy
run_test tests/scarborough_fair.cpy
