#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#ifdef _WIN32
    #include <malloc.h>
#elif __linux__
    #include <malloc.h>
#elif __APPLE__
    #include <stdlib.h>
#endif

#define MAXLEN 256

char *rename_file(char *filename, char suffix[]) {
    char *p1 = strrchr(filename, '/');
    p1 += 1;
    int len = strlen(p1);
    int suffix_len = strlen(suffix);
    char *newfile = (char *) malloc(MAXLEN * sizeof(char *));
    newfile = strncpy(newfile, p1, len - suffix_len);
    newfile[len - suffix_len] = '\0';
    return newfile;
}

// 判断字符串是否以指定后缀结尾的函数
int endsWith(char *str, char *suffix) {
    int str_len = strlen(str);
    int suffix_len = strlen(suffix);
    if (str_len < suffix_len) {
        return 0;
    }
    return (strcmp(str + str_len - suffix_len, suffix) == 0);
}

// 判断元素是否以指定的后缀结尾的函数
int endsWithAny(char *str, char *suffixes[], int num_suffixes) {
    for (int i = 0; i < num_suffixes; i++) {
        if (endsWith(str, suffixes[i])) {
            return 1;  // 返回1表示以指定的后缀结尾
        }
    }
    return 0;  // 返回0表示不以指定的后缀结尾
}

static PyObject *py_create(PyObject *self, PyObject *args) {
    char *input_name;
    char *output_name;
    int flag;
    if (!PyArg_ParseTuple(args, "ssi", &input_name, &output_name, &flag)) {
        return NULL;
    }
    clock_t start_time, end_time;
    double cpu_time_used;
    start_time = clock();
    FILE *fp = fopen(input_name, "r");
    if (fp == NULL) {
        fprintf(stderr, "can't open file %s", input_name);
    }
    FILE *fo = fopen(output_name, "w");
    char line[MAXLEN];
    char temp[MAXLEN];
    char seq1[MAXLEN];
    char seq2[MAXLEN];
    double distance;
    int num_seqs = 0;
    fgets(line, MAXLEN, fp);
    char pre_seq[MAXLEN];
    fgets(line, MAXLEN, fp);
    sscanf(line, "%s", temp);
    strcpy(pre_seq, temp);
    rewind(fp);
    fgets(line, MAXLEN, fp);
    char **seq_names = NULL;
    int max_num = 1000;
    seq_names = (char **) malloc(max_num * sizeof(char *));
    if (seq_names == NULL) {
        fprintf(stderr, "memory malloc error!\n");
    }
    while (fgets(line, MAXLEN, fp) != NULL) {
        sscanf(line, "%s %s", seq1, seq2);
        if (strcmp(pre_seq, seq1) != 0) {
            break;
        }
        if (num_seqs >= max_num) {
            max_num *= 2;
            seq_names = (char **) realloc(seq_names, max_num * sizeof(char *));
            if (seq_names == NULL) {
                fprintf(stderr, "memory malloc error!\n");
            }
        }
        seq_names[num_seqs] = (char *) malloc((strlen(seq2) + 1) * sizeof(char));
        if (seq_names[num_seqs] == NULL) {
            fprintf(stderr, "memory malloc error!\n");
        }
        strcpy(seq_names[num_seqs], seq2);
        num_seqs++;
    }
    double **distances = malloc(num_seqs * sizeof(double *));
    if (flag == 0) {
        for (int i = 0; i < num_seqs; i++) {
            distances[i] = malloc((i + 1) * sizeof(double));
            for (int j = 0; j <= i; j++)
                distances[i][j] = 0.0;
        }
    } else {
        for (int i = 0; i < num_seqs; i++) {
            distances[i] = malloc(i * sizeof(double));
            for (int j = 0; j < i; j++)
                distances[i][j] = 0.0;
        }
    }
    rewind(fp);
    fgets(line, MAXLEN, fp);
    int i = 0;
    int j = 0;
    if (flag == 0) {
        while (fgets(line, MAXLEN, fp) != NULL) {
            sscanf(line, "%*s %*s %*s %*s %lf", &distance);
            if (j <= i) {
                distances[i][j] = distance;
            }
            i += 1;
            if (i == num_seqs && j < num_seqs) {
                i = 0;
                j += 1;
            }
        }
    } else {
        while (fgets(line, MAXLEN, fp) != NULL) {
            sscanf(line, "%*s %*s %*s %*s %lf", &distance);
            if (j < i) {
                distances[i][j] = distance;
            }
            i += 1;
            if (i == num_seqs && j < num_seqs) {
                i = 0;
                j += 1;
            }
        }
    }

    for (int i = 0; i < num_seqs; i++) {
        char *suffixes[] = {".fasta.gz", ".fasta", ".fastq.gz", ".fastq", ".fna.gz", ".fna", ".fa.gz", ".fa"};
        int num_suffixes = 8;
        // 检查元素是否以指定的后缀结尾
        if (endsWithAny(seq_names[i], suffixes, num_suffixes)) {
            char *new_name = NULL;
            for (int k = 0; k < num_suffixes; k++) {
                char *p = strstr(seq_names[i], suffixes[k]);
                if (p != NULL) {
                    new_name = rename_file(seq_names[i], suffixes[k]);
                    break;
                }
            }
            seq_names[i] = strcpy(seq_names[i], new_name);
            if (new_name != NULL) {
                free(new_name);
            }
        }
    }


//    for (int i = 0; i < num_seqs; i++) {
//        for (int j = 0; j < num_seqs; j++) {
//            if (j <= i) {
//                printf("%.6f ", distances[i][j]);
//            }
//        }
//        printf("\n");
//    }
    fprintf(fo, "%d\n", num_seqs);
    if (flag == 0) {
        for (int i = 0; i < num_seqs; i++) {
            fprintf(fo, "%s\t", seq_names[i]);
            for (int j = 0; j < num_seqs; j++) {
                if (j <= i) {
                    fprintf(fo, "%.6f\t", distances[i][j]);
                }
            }
            fprintf(fo, "\n");
        }
    } else {
        for (int i = 0; i < num_seqs; i++) {
            fprintf(fo, "%s\t", seq_names[i]);
            for (int j = 0; j < num_seqs; j++) {
                if (j < i) {
                    fprintf(fo, "%.6f\t", distances[i][j]);
                }
            }
            fprintf(fo, "\n");
        }
    }
    for (int i = 0; i < num_seqs; i++) {
        free(distances[i]);
        free(seq_names[i]);
    }
    input_name = NULL;
    output_name = NULL;
    free(seq_names);
    free(distances);
    fclose(fp);
    fclose(fo);
    end_time = clock();
    cpu_time_used = ((double) (end_time - start_time)) / CLOCKS_PER_SEC;
    printf("create matrix runtime: %fs\n", cpu_time_used);
    return Py_BuildValue("i", num_seqs);
}

static PyMethodDef MatrixUtilsMethods[] = {
        {"create", py_create, METH_VARARGS, "create"},
        {NULL, NULL,          0, NULL}
};

static struct PyModuleDef matrixutilsmodule = {
        PyModuleDef_HEAD_INIT,
        "matrixutils",           /* name of module */
        "A matrixutils module",  /* Doc string (may be NULL) */
        -1,                      /* Size of per-interpreter state or -1 */
        MatrixUtilsMethods       /* Method table */
};

PyMODINIT_FUNC PyInit_matrixutils(void) {
    return PyModule_Create(&matrixutilsmodule);
}