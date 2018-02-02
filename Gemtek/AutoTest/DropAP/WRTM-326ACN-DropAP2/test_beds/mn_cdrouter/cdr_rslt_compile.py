__author__ = 'bmelhus'

def add_to_rslt_file(cdr_rslt_file, rslt_info):

    f1 = "/opt/home/bmelhus/stp/test_beds/mn_cdrouter/results/cdr_results/" + str(cdr_rslt_file)

    with open(f1, "a") as myfile:
        myfile.write(rslt_info + "\n")
