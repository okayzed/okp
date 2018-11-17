tests_to_run=$*

function run_test() {
  if ! [[ ${1} =~ ${tests_to_run} ]]; then
    return
  fi
  name=${1/.cpy/.cpp}
  exe_name=${name/.cpp/.exe}
  in_name=${name/.cpp/.in}
  out_name=${name/.cpp/.out}
  tmp_name=${name/.cpp/.tmp}
  diff_name=${name/.cpp/.diff}
  FLAGS="--enable-for --enable-rof"

  python -m okp.main - $FLAGS < ${1} > "${name}"
  g++ -x c++ - -o ${exe_name} < "${name}"
  if [[ $? != 0 ]]; then
    cat -n "${name}"
    echo "FAILED: ${1}"
  else

    prefix="-"
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
      prefix="+"
    fi

    echo "${prefix}PASSED: ${1}"
  fi
}


function basic_tests() {
  run_test tests/basic_main.cpy
  run_test tests/basic_class.cpy
  run_test tests/parens.cpy
  run_test tests/loop_shorthand.cpy
  run_test tests/params_test.cpy
  run_test tests/toplevel_invoke.cpy
  run_test tests/nested_identifiers.cpy
  run_test tests/known_vars.cpy
  run_test tests/demo_program.cpy
  run_test tests/class_constructors.cpy
	run_test tests/switch_statement.cpy
  run_test tests/long_conditionals.cpy # aka joined lines
  run_test tests/function_with_comments_after.cpy
  run_test tests/recognize_struct.cpy
  run_test tests/infer_includes.cpy
  run_test tests/ignore_lines.cpy
}

function external_tests() {

	# from CPY
	run_test tests/external/cpy_readme.cpy
  run_test tests/external/quick_print.cpy
  run_test tests/external/example_class.cpy
  run_test tests/external/simple_array_max_min.cpy
  run_test tests/external/scarborough_fair.cpy

	# elsewhere
  run_test tests/external/c_look_like_python.cpy
  run_test tests/external/manacher.cpy
  run_test tests/external/tree_diameter2.cpy
  run_test tests/external/cocktail_sort.cpy
}

basic_tests
external_tests
