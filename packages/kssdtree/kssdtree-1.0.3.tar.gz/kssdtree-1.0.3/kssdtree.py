import kssdutils
import njutils
import dnjutils
import matrixutils

import kssdtree
import toolutils
import os
import platform
import shutil
import stat
import time


def shuffle(k=8, s=5, l=2, o='default'):
    print('shuffling...')
    kssdutils.write_dim_shuffle_file(k, s, l, o)
    print('shuffle finished!')


def sketch(shuf_file=None, genome_files=None, output_sketch=None, set_operation=False):
    if shuf_file is not None and genome_files is not None and output_sketch is not None:
        current_directory = os.getcwd()
        shuf_file_path = os.path.join(current_directory, shuf_file)
        if not os.path.exists(shuf_file_path):
            file_name = shuf_file.split('.')[0]
            k = int(shuf_file.split('.')[0][3:])
            if k == 10:
                s = 6
            else:
                s = 5
            l = int(shuf_file[1])
            shuffle(k=k, s=s, l=l, o=file_name)
        print('sketching...')
        start = time.time()
        if set_operation:
            kssdutils.dist_dispatch(shuf_file, genome_files, output_sketch, 1, 0)
        else:
            kssdutils.dist_dispatch(shuf_file, genome_files, output_sketch, 0, 0)
        end = time.time()
        print('sketch spend time：%.2fs' % (end - start))
        print('sketch finished!')
    else:
        print('args error!!!')


def union(reference_sketch=None, output_sketch=None):
    if reference_sketch is not None and output_sketch is not None:
        print('unioning...')
        start = time.time()
        kssdutils.sketch_union(reference_sketch, output_sketch)
        end = time.time()
        print('union spend time：%.2fs' % (end - start))
        print('union finished!')
    else:
        print('args error!!!')


def subtract(reference_sketch=None, genomes_sketch=None, output_sketch=None):
    if reference_sketch is not None and genomes_sketch is not None and output_sketch is not None:
        print('subtracting...')
        start = time.time()
        kssdutils.sketch_operate(reference_sketch, output_sketch, genomes_sketch)
        end = time.time()
        print('subtract spend time：%.2fs' % (end - start))
        print('subtract finished!')
    else:
        print('args error!!!')


def dist(genomes_sketch=None, output_dist=None):
    if genomes_sketch is not None and output_dist is not None:
        print('disting...')
        start = time.time()
        kssdutils.dist_dispatch(genomes_sketch, output_dist, genomes_sketch, 2, 0)
        end = time.time()
        print('dist spend time：%.2fs' % (end - start))
        print('dist finished!')
    else:
        print('args error!!!')


def dist_N(ref_sketch=None, qry_sketch=None, output_dist=None, N=0):
    # kssdtree.dist_N(ref_sketch='gtdb_sketch', qry_sketch='new_genomes_sketch', output_dist='test_distout', N=10)
    if ref_sketch is not None and qry_sketch is not None and output_dist is not None:
        print('dist_Ning...')
        start = time.time()
        kssdutils.dist_dispatch(ref_sketch, output_dist, qry_sketch, 2, N)
        end = time.time()
        print('dist_N spend time：%.2fs' % (end - start))
        print('dist_N finished!')
    else:
        print('args error or N<=0!!!')


def combine(sketch1=None, sketch2=None, output_sketch=None):
    # kssdtree.combine(sketch1='new_genomes_sketch', sketch2='related_genomes_sketch', output_sketch='test_combine')
    if sketch1 is not None and sketch2 is not None and output_sketch is not None:
        print('combining...')
        start = time.time()
        kssdutils.dist_dispatch(output_sketch, sketch1, sketch2, 3, 0)
        end = time.time()
        print('combine spend time：%.2fs' % (end - start))
        print('combine finished!')
    else:
        print('args error!!!')


def genome_txt(input_sketch=None, output_txt=None):
    # kssdtree.genome_txt(input_sketch='gtdbr214_sketch', output_txt='test.txt')
    if input_sketch is not None and output_txt:
        print('printing...')
        start = time.time()
        kssdutils.print_gnames(input_sketch, output_txt)
        end = time.time()
        print('print spend time：%.2fs' % (end - start))
        print('print finished!')
    else:
        print('args error!!!')


def genome_group(input_txt, genomes_sketch, output_sketch):
    # kssdtree.genome_group(input_txt='new_gtdbr214.txt', genomes_sketch='gtdbr214_sketch', output_sketch='re_sketch')
    if input_txt is not None and genomes_sketch is not None and output_sketch is not None:
        print('grouping...')
        start = time.time()
        kssdutils.grouping_genomes(input_txt, genomes_sketch, output_sketch)
        end = time.time()
        print('group spend time：%.2fs' % (end - start))
        print('group finished!')
    else:
        print('args error!!!')


def build(input_dist=None, output=None, method='nj', mode='r'):
    if method not in ['nj', 'dnj']:
        print('method only support nj and dnj!!!')
        return
    if mode not in ['r', 'c']:
        # Valid modes are 'c'(ircular)  or 'r'(ectangular)
        print('mode only support r(rectangular) and c(circular)!!!')
        return
    if input_dist is not None:
        print('building...')
        start = time.time()
        temp_distance = input_dist + '.phy'
        file_path = os.path.join(os.getcwd(), input_dist, 'distance.out')
        current_directory = os.getcwd()
        temp_distance_path = os.path.join(current_directory, temp_distance)
        if output is None:
            output = 'kssdtree.newick'
        if os.path.exists(temp_distance_path):
            os.remove(temp_distance_path)
        if method == 'nj':
            genome_nums = matrixutils.create(file_path, temp_distance, 0)
            state = njutils.build(temp_distance, output)
        else:
            genome_nums = matrixutils.create(file_path, temp_distance, 1)
            state = dnjutils.build(temp_distance, output, method)
        if state == 1:
            end = time.time()
            print('build spend time：%.2fs' % (end - start))
            print('build finished!')
            nwk_path = os.path.join(os.getcwd(), output)
            with open(nwk_path, 'r') as f:
                lines = f.readlines()
                merged_line = ''.join(lines)
                merged_line = merged_line.replace('\n', '')
            with open(nwk_path, 'w') as f:
                f.write(merged_line)
            if platform.system() == 'Linux':
                pass
            else:
                print('genome_nums: ', genome_nums)
                print('tree visualization finished!')
                toolutils.view_general_tree(nwk_path, mode=mode)
    else:
        print('args error!!!')


def quick(shuf_file=None, genome_files=None, output=None, reference=None, taxonomy_txt=None, method='nj', mode='r',
          N=0):
    # kssdtree.quick(shuf_file='L3K9.shuf', genome_files='new_genomes', output='new_genomes.newick', reference='gtdb_sketch', method='nj', mode='r', N=10)
    if reference is None and taxonomy_txt is None:
        if shuf_file is not None and genome_files is not None and output is not None:
            timeStamp = int(time.mktime(time.localtime(time.time())))
            temp_genome_sketch = genome_files + '_sketch_' + str(timeStamp)
            temp_dist_output = genome_files + '_distout'
            print('step1...')
            kssdtree.sketch(shuf_file=shuf_file, genome_files=genome_files, output_sketch=temp_genome_sketch,
                            set_operation=False)
            print('step2...')
            kssdtree.dist(genomes_sketch=temp_genome_sketch, output_dist=temp_dist_output)
            print('step3...')
            kssdtree.build(input_dist=temp_dist_output, output=output, method=method, mode=mode)
            current_directory = os.getcwd()
            temp_dir1 = os.path.join(current_directory, temp_genome_sketch)
            temp_dir2 = os.path.join(current_directory, temp_dist_output)
            if platform.system() == 'Linux':
                if os.path.exists(temp_dir1):
                    shutil.rmtree(temp_dir1)
                if os.path.exists(temp_dir2):
                    shutil.rmtree(temp_dir2)
            else:
                if os.path.exists(temp_dir1):
                    try:
                        shutil.rmtree(temp_dir1)
                    except PermissionError as e:
                        err_file_path = str(e).split("\'", 2)[1]
                        if os.path.exists(err_file_path):
                            os.chmod(err_file_path, stat.S_IWRITE)
                if os.path.exists(temp_dir2):
                    try:
                        shutil.rmtree(temp_dir2)
                    except PermissionError as e:
                        err_file_path = str(e).split("\'", 2)[1]
                        if os.path.exists(err_file_path):
                            os.chmod(err_file_path, stat.S_IWRITE)
                # for temp_dir in [temp_dir1, temp_dir2]:
                #     while os.path.exists(temp_dir):
                #         try:
                #             shutil.rmtree(temp_dir)
                #         except PermissionError as e:
                #             err_file_path = str(e).split("\'", 2)[1]
                #             if os.path.exists(err_file_path):
                #                 os.chmod(err_file_path, stat.S_IWRITE)
                #             else:
                #                 break
        else:
            print('args error!!!')
    elif reference == "gtdb_sketch" and taxonomy_txt is None:
        if shuf_file is not None and genome_files is not None and output is not None and toolutils.is_positive_integer(
                N):
            timeStamp = int(time.mktime(time.localtime(time.time())))
            temp_genome_sketch = genome_files + '_sketch_' + str(timeStamp)
            temp_dist_output = genome_files + '_' + str(N) + '_distout'
            temp_related_sketch = genome_files + '_related_sketch_' + str(timeStamp)
            temp_combine_sketch = 'combine_sketch_' + str(timeStamp)
            temp_combine_dist_output = 'combine_distout'
            temp_distance_matrix = 'new_gtdb.phy'
            kssdtree.sketch(shuf_file=shuf_file, genome_files=genome_files, output_sketch=temp_genome_sketch,
                            set_operation=False)
            kssdtree.dist_N(ref_sketch=reference, qry_sketch=temp_genome_sketch, output_dist=temp_dist_output, N=N)
            kssdtree.genome_txt(input_sketch=reference, output_txt='gtdb.txt')
            file_path1 = os.path.join(os.getcwd(), temp_dist_output, 'distance.out')
            toolutils.deal_gtdb_txt(file_path1)
            kssdtree.genome_group(input_txt='new_gtdb.txt', genomes_sketch=reference, output_sketch=temp_related_sketch)
            kssdtree.combine(sketch1=temp_genome_sketch, sketch2=temp_related_sketch, output_sketch=temp_combine_sketch)
            kssdtree.dist(genomes_sketch=temp_combine_sketch, output_dist=temp_combine_dist_output)
            file_path2 = os.path.join(os.getcwd(), temp_combine_dist_output, 'distance.out')
            if method == 'nj':
                genome_nums = matrixutils.create(file_path2, temp_distance_matrix, 0)
            else:
                genome_nums = matrixutils.create(file_path2, temp_distance_matrix, 1)
            toolutils.deal_gtdb_phy(temp_distance_matrix)
            print('building...')
            start = time.time()
            if method == 'nj':
                state = njutils.build(temp_distance_matrix, output)
            else:
                state = dnjutils.build(temp_distance_matrix, output, method)
            if state == 1:
                end = time.time()
                print('build spend time：%.2fs' % (end - start))
                print('build finished!')
                nwk_path = os.path.join(os.getcwd(), output)
                with open(nwk_path, 'r') as f:
                    lines = f.readlines()
                    merged_line = ''.join(lines)
                    merged_line = merged_line.replace('\n', '')
                with open(nwk_path, 'w') as f:
                    f.write(merged_line)
                if platform.system() == 'Linux':
                    pass
                else:
                    print('genome_nums: ', genome_nums)
                    print('tree visualization finished!')
                    toolutils.view_gtdb_tree(temp_distance_matrix, nwk_path, mode)
                file_path1 = 'new.txt'
                file_path2 = 'gtdb.txt'
                file_path3 = 'new_gtdb.txt'
                file_path4 = 'related_genomes_values.txt'
                file_path5 = 'modified_file.txt'
                if os.path.exists(file_path1):
                    os.remove(file_path1)
                if os.path.exists(file_path2):
                    os.remove(file_path2)
                if os.path.exists(file_path3):
                    os.remove(file_path3)
                if os.path.exists(file_path4):
                    os.remove(file_path4)
                if os.path.exists(file_path5):
                    os.remove(file_path5)
                current_directory = os.getcwd()
                temp_dir1 = os.path.join(current_directory, temp_genome_sketch)
                temp_dir2 = os.path.join(current_directory, temp_dist_output)
                temp_dir3 = os.path.join(current_directory, temp_related_sketch)
                temp_dir4 = os.path.join(current_directory, temp_combine_sketch)
                temp_dir5 = os.path.join(current_directory, temp_combine_dist_output)
                if platform.system() == 'Linux':
                    if os.path.exists(temp_dir1):
                        shutil.rmtree(temp_dir1)
                    if os.path.exists(temp_dir2):
                        shutil.rmtree(temp_dir2)
                    if os.path.exists(temp_dir3):
                        shutil.rmtree(temp_dir3)
                    if os.path.exists(temp_dir4):
                        shutil.rmtree(temp_dir4)
                    if os.path.exists(temp_dir5):
                        shutil.rmtree(temp_dir5)
                else:
                    pass
        else:
            print('args error or N<=0!!!')
    else:
        if shuf_file is not None and genome_files is not None and output is not None:
            timeStamp = int(time.mktime(time.localtime(time.time())))
            temp_reference_sketch = 'ref_sketch_' + str(timeStamp)
            temp_genomes_sketch = genome_files + '_sketch_' + str(timeStamp)
            cur_path = os.getcwd()
            ref_path = os.path.join(cur_path, reference)
            num = toolutils.get_all(ref_path)
            if num == 1:
                temp_union_sketch = temp_reference_sketch
            else:
                temp_union_sketch = 'ref_union_sketch_' + str(timeStamp)
            temp_subtract_sketch = genome_files + '_subtract_sketch_' + str(timeStamp)
            temp_dist_output = genome_files + '_distout'
            print('step1...')
            kssdtree.sketch(shuf_file=shuf_file, genome_files=reference, output_sketch=temp_reference_sketch,
                            set_operation=True)
            kssdtree.sketch(shuf_file=shuf_file, genome_files=genome_files, output_sketch=temp_genomes_sketch,
                            set_operation=True)
            print('step2...')
            kssdtree.union(reference_sketch=temp_reference_sketch, output_sketch=temp_union_sketch)
            print('step3...')
            kssdtree.subtract(reference_sketch=temp_union_sketch, genomes_sketch=temp_genomes_sketch,
                              output_sketch=temp_subtract_sketch)
            print('step4...')
            kssdtree.dist(genomes_sketch=temp_subtract_sketch, output_dist=temp_dist_output)
            print('step5...')
            if taxonomy_txt is None:
                kssdtree.build(input_dist=temp_dist_output, output=output, method=method, mode=mode)
            else:
                temp_distance_matrix = genome_files + '.phy'
                file_path2 = os.path.join(os.getcwd(), temp_dist_output, 'distance.out')
                if method == 'nj':
                    genome_nums = matrixutils.create(file_path2, temp_distance_matrix, 0)
                else:
                    genome_nums = matrixutils.create(file_path2, temp_distance_matrix, 1)
                print('building...')
                start = time.time()
                if method == 'nj':
                    state = njutils.build(temp_distance_matrix, output)
                else:
                    state = dnjutils.build(temp_distance_matrix, output, method)
                if state == 1:
                    end = time.time()
                    print('build spend time：%.2fs' % (end - start))
                    print('build finished!')
                    nwk_path = os.path.join(os.getcwd(), output)
                    with open(nwk_path, 'r') as f:
                        lines = f.readlines()
                        merged_line = ''.join(lines)
                        merged_line = merged_line.replace('\n', '')
                    with open(nwk_path, 'w') as f:
                        f.write(merged_line)
                    if platform.system() == 'Linux':
                        pass
                    else:
                        print('genome_nums: ', genome_nums)
                        print('tree visualization finished!')
                        toolutils.view_pan_tree(taxonomy_txt=taxonomy_txt, nwk_path=nwk_path, mode=mode)
            current_directory = os.getcwd()
            temp_dir1 = os.path.join(current_directory, temp_reference_sketch)
            temp_dir2 = os.path.join(current_directory, temp_genomes_sketch)
            temp_dir3 = os.path.join(current_directory, temp_union_sketch)
            temp_dir4 = os.path.join(current_directory, temp_subtract_sketch)
            temp_dir5 = os.path.join(current_directory, temp_dist_output)
            if platform.system() == 'Linux':
                if os.path.exists(temp_dir1):
                    shutil.rmtree(temp_dir1)
                if os.path.exists(temp_dir2):
                    shutil.rmtree(temp_dir2)
                if os.path.exists(temp_dir3):
                    shutil.rmtree(temp_dir3)
                if os.path.exists(temp_dir4):
                    shutil.rmtree(temp_dir4)
                if os.path.exists(temp_dir5):
                    shutil.rmtree(temp_dir5)
            else:
                pass
        else:
            print('args error!!!')
