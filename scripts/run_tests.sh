mkdir -p compiled/tests

function run_test() {
  name=${1/.cpy/.cpp}
  exe_name=${name/.cpp/.exe}
  in_name=${name/.cpp/.in}
  out_name=${name/.cpp/.out}
  tmp_name=${name/.cpp/.tmp}
  diff_name=${name/.cpp/.diff}

  python src/main.py < ${1} > "${name}"
  g++ -x c++ - -o ${exe_name} < "${name}"
  if [[ $? != 0 ]]; then
    cat -n "compiled/${name}"
    echo "FAILED: ${1}"
  else

    if test -f ${in_name}; then
      # to regen output files:
      # if test -f ${out_name}; then
      #     cat ${in_name} | ${exe_name} > ${out_name}
      # fi
      cat ${in_name} | ${exe_name} > ${tmp_name}
    else
      ${exe_name} > ${tmp_name}
    fi

    if test -f ${out_name}; then
      diff ${out_name} ${tmp_name} > ${diff_name}
      if [[ $? != 0 ]]; then
        echo "FAILED: ${1}"
        cat ${diff_name}
        return
      fi
    fi

    echo "PASSED: ${1}"
  fi
}


function basic_tests() {
  run_test tests/basic_main.cpy
  run_test tests/basic_class.cpy
  run_test tests/params_test.cpy
  run_test tests/toplevel_invoke.cpy
  run_test tests/nested_identifiers.cpy
  run_test tests/known_vars.cpy
  run_test tests/demo_program.cpy
}

function external_tests() {
  run_test tests/quick_print.cpy
  run_test tests/example_class.cpy
  run_test tests/simple_array_max_min.cpy
  run_test tests/scarborough_fair.cpy
  run_test tests/c_look_like_python.cpy
  run_test tests/manacher.cpy
  run_test tests/tree_diameter2.cpy
}

basic_tests
external_tests
