#include <Python.h>
#include "kssdheaders/command_dist.h"
#include "kssdheaders/command_dist_wrapper.h"
#include "kssdheaders/command_shuffle.h"
#include "kssdheaders/global_basic.h"
#include "kssdheaders/command_set.h"
#include <stdio.h>
#include <string.h>

#ifdef _OPENMP
#include <omp.h>
#else
#define omp_get_thread_num() 0
#endif

dim_shuffle_stat_t dim_shuffle_stat = {
        0,
        8,
        5,
        2,
};
char shuf_out_file_prefix[PATHLEN] = "./default";

static PyObject *py_write_dim_shuffle_file(PyObject *self, PyObject *args) {
    int k, s, l;
    char *o;
    if (!PyArg_ParseTuple(args, "iiis", &k, &s, &l, &o)) {
        return NULL;
    }
    dim_shuffle_stat.k = k;
    dim_shuffle_stat.subk = s;
    dim_shuffle_stat.drlevel = l;
    strcpy(shuf_out_file_prefix, o);
    int state = write_dim_shuffle_file(&dim_shuffle_stat, shuf_out_file_prefix);
    return Py_BuildValue("i", state);
}


static PyObject *py_dist_dispatch(PyObject *self, PyObject *args) {
    char *str1;
    char *str2;
    char *str3;
    int flag;
    int N;
    if (!PyArg_ParseTuple(args, "sssii", &str1, &str2, &str3, &flag, &N)) {
        return NULL;
    }
    if (flag == 0) {
        dist_opt_val_t dist_opt_val1 =
                {
                        .k = 8,
                        .p = 0,
                        .dr_level = 2,
                        .dr_file = "",
                        .mmry = 0,
                        .fmt = "mfa",
                        .refpath = "",
                        .fpath = "",
                        .outdir = ".",
                        .kmerocrs = 1,
                        .kmerqlty = 0,
                        .keepco = false,
                        .stage2 = false,
                        .num_neigb = 0,
                        .mut_dist_max = 1,
                        .metric = Jcd,
                        .outfields = CI,
                        .correction = false,
                        .abundance = false,
                        .pipecmd = "",
                        .shared_kmerpath="",
                        .keep_shared_kmer=false,
                        .byread=false,
                        .num_remaining_args = 0,
                        .remaining_args = NULL
                };
        struct stat path_stat;
        if (stat(str1, &path_stat) >= 0 && S_ISREG(path_stat.st_mode)) {
            if (strlen(str1) < PATHLEN)
                strcpy(dist_opt_val1.dr_file, str1);
            else
                fprintf(stderr, "-L argument path should not longer than %d", PATHLEN);
        } else {
            if (atoi(str1) >= dist_opt_val1.k - 2 || atoi(str1) < 0)
                fprintf(stderr, "-L: dimension reduction level should never larger than Kmer length - 2,"
                                " which is %d here", dist_opt_val1.k - 2);
            dist_opt_val1.dr_level = atoi(str1);
        }
        strcpy(dist_opt_val1.refpath, str2);
        strcpy(dist_opt_val1.outdir, str3);
        dist_opt_val1.num_remaining_args = 0;
        dist_opt_val1.remaining_args = NULL;
#ifdef _OPENMP
        if(dist_opt_val1.p == 0)
            dist_opt_val1.p = omp_get_num_procs();
#else
        if (dist_opt_val1.p == 0)
            dist_opt_val1.p = 1;
#endif
//#ifdef _WIN32
//        double sys_mm = get_sys_mmry();
//        double rqst_mm = 2.0;
//        if (rqst_mm > sys_mm) {
//            fprintf(stderr, "Memory request is larger than system available %f. Ignoring -m %f", sys_mm, rqst_mm);
//            dist_opt_val1.mmry = sys_mm;
//        } else {
//            dist_opt_val1.mmry = rqst_mm;
//        }
//#endif
        int state1 = dist_dispatch(&dist_opt_val1);
    } else if (flag == 1) {
        dist_opt_val_t dist_opt_val2 =
                {
                        .k = 8,
                        .p = 0,
                        .dr_level = 2,
                        .dr_file = "",
                        .mmry = 0,
                        .fmt = "mfa",
                        .refpath = "",
                        .fpath = "",
                        .outdir = ".",
                        .kmerocrs = 1,
                        .kmerqlty = 0,
                        .keepco = false,
                        .stage2 = false,
                        .num_neigb = 0,
                        .mut_dist_max = 1,
                        .metric = Jcd,
                        .outfields = CI,
                        .correction = false,
                        .abundance = false,
                        .pipecmd = "",
                        .shared_kmerpath="",
                        .keep_shared_kmer=false,
                        .byread=false,
                        .num_remaining_args = 0,
                        .remaining_args = NULL
                };
        struct stat path_stat;
        if (stat(str1, &path_stat) >= 0 && S_ISREG(path_stat.st_mode)) {
            if (strlen(str1) < PATHLEN)
                strcpy(dist_opt_val2.dr_file, str1);
            else
                fprintf(stderr, "-L argument path should not longer than %d", PATHLEN);
        }
        strcpy(dist_opt_val2.outdir, str3);
        dist_opt_val2.num_remaining_args = 1;
        dist_opt_val2.remaining_args = &str2;
#ifdef _OPENMP
        if(dist_opt_val2.p == 0)
            dist_opt_val2.p = omp_get_num_procs();
#else
        if (dist_opt_val2.p == 0)
            dist_opt_val2.p = 1;
#endif
//#ifdef _WIN32
//        double sys_mm = get_sys_mmry();
//        double rqst_mm = 2.0;
//        if (rqst_mm > sys_mm) {
//            fprintf(stderr, "Memory request is larger than system available %f. Ignoring -m %f", sys_mm, rqst_mm);
//            dist_opt_val2.mmry = sys_mm;
//        } else {
//            dist_opt_val2.mmry = rqst_mm;
//        }
//#endif
        int state2 = dist_dispatch(&dist_opt_val2);
    } else if (flag == 2){
        dist_opt_val_t dist_opt_val3 =
                {
                        .k = 8,
                        .p = 0,
                        .dr_level = 2,
                        .dr_file = "",
                        .mmry = 0,
                        .fmt = "mfa",
                        .refpath = "",
                        .fpath = "",
                        .outdir = ".",
                        .kmerocrs = 1,
                        .kmerqlty = 0,
                        .keepco = false,
                        .stage2 = false,
                        .num_neigb = 0,
                        .mut_dist_max = 1,
                        .metric = Jcd,
                        .outfields = CI,
                        .correction = false,
                        .abundance = false,
                        .pipecmd = "",
                        .shared_kmerpath="",
                        .keep_shared_kmer=false,
                        .byread=false,
                        .num_remaining_args = 0,
                        .remaining_args = NULL
                };
        strcpy(dist_opt_val3.refpath, str1);
        strcpy(dist_opt_val3.outdir, str2);
        dist_opt_val3.num_remaining_args = 1;
        dist_opt_val3.remaining_args = &str3;
        dist_opt_val3.num_neigb = N;
#ifdef _OPENMP
        if(dist_opt_val3.p == 0)
            dist_opt_val3.p = omp_get_num_procs();
#else
        if (dist_opt_val3.p == 0)
            dist_opt_val3.p = 1;
#endif
//#ifdef _WIN32
//        double sys_mm = get_sys_mmry();
//        double rqst_mm = 6.5;
//        printf("sys_mm: %f GB\n", sys_mm);
//        printf("rqst_mm: %f GB\n", rqst_mm);
//        if (rqst_mm > sys_mm) {
//            fprintf(stderr, "Memory request is larger than system available %f. Ignoring -m %f", sys_mm, rqst_mm);
//            dist_opt_val3.mmry = sys_mm;
//        } else {
//            dist_opt_val3.mmry = rqst_mm;
//        }
//#endif
        int state3 = dist_dispatch(&dist_opt_val3);
    } else {
        dist_opt_val_t dist_opt_val4 =
                {
                        .k = 8,
                        .p = 0,
                        .dr_level = 2,
                        .dr_file = "",
                        .mmry = 0,
                        .fmt = "mfa",
                        .refpath = "",
                        .fpath = "",
                        .outdir = ".",
                        .kmerocrs = 1,
                        .kmerqlty = 0,
                        .keepco = false,
                        .stage2 = false,
                        .num_neigb = 0,
                        .mut_dist_max = 1,
                        .metric = Jcd,
                        .outfields = CI,
                        .correction = false,
                        .abundance = false,
                        .pipecmd = "",
                        .shared_kmerpath="",
                        .keep_shared_kmer=false,
                        .byread=false,
                        .num_remaining_args = 0,
                        .remaining_args = malloc(2 * sizeof(char *))
                };
        strcpy(dist_opt_val4.outdir, str1);
        dist_opt_val4.num_remaining_args = 2;
        dist_opt_val4.remaining_args[0] = str2;
        dist_opt_val4.remaining_args[1] = str3;
#ifdef _OPENMP
        if(dist_opt_val4.p == 0)
            dist_opt_val4.p = omp_get_num_procs();
#else
        if (dist_opt_val4.p == 0)
            dist_opt_val4.p = 1;
#endif
//#ifdef _WIN32
//        double sys_mm = get_sys_mmry();
//        double rqst_mm = 2.0;
//        if (rqst_mm > sys_mm) {
//            fprintf(stderr, "Memory request is larger than system available %f. Ignoring -m %f", sys_mm, rqst_mm);
//            dist_opt_val4.mmry = sys_mm;
//        } else {
//            dist_opt_val4.mmry = rqst_mm;
//        }
//#endif
        int state4 = dist_dispatch(&dist_opt_val4);
    }
    str1 = NULL;
    str2 = NULL;
    str3 = NULL;
    return Py_BuildValue("i", 1);
}


static PyObject *py_sketch_union(PyObject *self, PyObject *args) {
    char *i;
    char *o;
    if (!PyArg_ParseTuple(args, "ss", &i, &o)) {
        return NULL;
    }
    set_opt_t set_opt1 = {
            .operation = -1,
            .p = 1,
            .P = 0,
            .num_remaining_args = 0,
            .remaining_args = NULL,
            .insketchpath = "",
            .pansketchpath="",
            .subsetf[0] = '\0',
            .outdir = ""
    };
    strcpy(set_opt1.insketchpath, i);
    strcpy(set_opt1.outdir, o);
    int state = sketch_union(set_opt1);
    i = NULL;
    o = NULL;
    return Py_BuildValue("i", state);
}


static PyObject *py_sketch_sub(PyObject *self, PyObject *args) {
    char *i;
    char *o;
    char *remain;
    if (!PyArg_ParseTuple(args, "sss", &i, &o, &remain)) {
        return NULL;
    }
    set_opt_t set_opt2 = {
            .operation = -1,
            .p = 1,
            .P = 0,
            .num_remaining_args = 0,
            .remaining_args = NULL,
            .insketchpath = "",
            .pansketchpath="",
            .subsetf[0] = '\0',
            .outdir = ""
    };
    strcpy(set_opt2.pansketchpath, i);
    strcpy(set_opt2.outdir, o);
    strcpy(set_opt2.insketchpath, remain);
    set_opt2.num_remaining_args = 1;
    set_opt2.remaining_args = &remain;
    int state = sketch_operate(set_opt2);
    set_opt2.num_remaining_args = 0;
    set_opt2.remaining_args = NULL;
    i = NULL;
    o = NULL;
    remain = NULL;
    return Py_BuildValue("i", state);
}


static PyObject *py_sketch_print(PyObject *self, PyObject *args) {
    char *o;
    char *remain;
    if (!PyArg_ParseTuple(args, "ss", &remain, &o)) {
        return NULL;
    }
    set_opt_t set_opt3 = {
            .operation = -1,
            .p = 1,
            .P = 0,
            .num_remaining_args = 0,
            .remaining_args = NULL,
            .insketchpath = "",
            .pansketchpath="",
            .subsetf[0] = '\0',
            .outdir = ""
    };
    set_opt3.P = 1;
    strcpy(set_opt3.insketchpath, remain);
    set_opt3.num_remaining_args = 1;
    set_opt3.remaining_args = &remain;
    print_gnames(set_opt3, o);
    set_opt3.num_remaining_args = 0;
    set_opt3.remaining_args = NULL;
    o = NULL;
    remain = NULL;
    return Py_BuildValue("i", 1);
}


static PyObject *py_sketch_group(PyObject *self, PyObject *args) {
    char *i;
    char *o;
    char *remain;
    if (!PyArg_ParseTuple(args, "sss", &i, &remain, &o)) {
        return NULL;
    }
    set_opt_t set_opt4 = {
            .operation = -1,
            .p = 1,
            .P = 0,
            .num_remaining_args = 0,
            .remaining_args = NULL,
            .insketchpath = "",
            .pansketchpath="",
            .subsetf[0] = '\0',
            .outdir = ""
    };
    strcpy(set_opt4.subsetf, i);
    strcpy(set_opt4.outdir, o);
    strcpy(set_opt4.insketchpath, remain);
    set_opt4.num_remaining_args = 1;
    set_opt4.remaining_args = &remain;
    int state = grouping_genomes(set_opt4, i);
    set_opt4.num_remaining_args = 0;
    set_opt4.remaining_args = NULL;
    i = NULL;
    o = NULL;
    remain = NULL;
    return Py_BuildValue("i", state);
}



static PyMethodDef KssdutilsMethods[] = {
        {"write_dim_shuffle_file", py_write_dim_shuffle_file, METH_VARARGS, "shuffle"},
        {"dist_dispatch",          py_dist_dispatch,          METH_VARARGS, "sketch and dist"},
        {"sketch_union",           py_sketch_union,           METH_VARARGS, "sketch union"},
        {"sketch_operate",         py_sketch_sub,             METH_VARARGS, "sketch sub"},
        {"print_gnames",           py_sketch_print,           METH_VARARGS, "sketch print"},
        {"grouping_genomes",       py_sketch_group,           METH_VARARGS, "sketch group"},
        {NULL, NULL,                                          0, NULL}
};

static struct PyModuleDef kssdutilsmodule = {
        PyModuleDef_HEAD_INIT,
        "kssdutils",           /* name of module */
        "A kssdutils module",  /* Doc string (may be NULL) */
        -1,               /* Size of per-interpreter state or -1 */
        KssdutilsMethods       /* Method table */
};

PyMODINIT_FUNC PyInit_kssdutils(void) {
    return PyModule_Create(&kssdutilsmodule);
}