$(function() {
    $(".suite_header").click(function() {
        $(this).siblings(".tc_table").toggle();
    });

    $(".tc_header").click(function() {
        $(this).siblings(".step_table").toggle();
    });

    $(".step_header").click(function() {
        $(this).siblings(".step_detail_table").toggle();
    });
});