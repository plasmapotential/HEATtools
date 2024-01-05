#goes thru all directories with a prefix and pulls out the .vtp files
#then copies them into an output dir

import os 
import shutil

rootPath = '/home/tlooby/HEAT/data/'
prefix = 'sparc_000001_ILIM_NX_ellipse1mm_'
outDir = rootPath + prefix + 'VTPs/'
name = 'HF_optical_all_mesh'


def copyVTPFilesInPrefixDirs(root_path, prefix, out_dir, name):
    """
    Copy a file from subdirectories that contain a specific prefix to an output directory,
    renaming the file by appending the second half of the subdirectory's name.

    :param root_path: Path to the main directory.
    :param prefix: The prefix in the subdirectory names to look for.
    :param out_dir: The directory where the files will be copied to.
    """
    # Ensure the output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # Iterate through items in the root directory
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)

        # Check if the item is a directory and has the prefix
        if os.path.isdir(item_path) and item.startswith(prefix):
            id = item.split('_')[-1]
            if id == 'VTPs':
                continue
            else:
                filename = root_path + item + '/000001/paraview/' + name + '.vtp'
                new_filename = out_dir + name + '_' + id + '.vtp'
                # Copy the file
                try:
                    if os.path.exists(out_dir):
                        shutil.copy(filename, new_filename)
                    else:
                        print(f"File not found: {out_dir}")
                except:
                    print("NO file")


copyVTPFilesInPrefixDirs(rootPath, prefix, outDir, name)
print("Copied VTPs...")
