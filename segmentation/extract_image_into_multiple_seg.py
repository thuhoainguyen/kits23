import os
import nibabel as nib
import numpy as np

NII_IMG_PATH = "dataset_histology_preprocessed/case_00016/segmentation.nii.gz"
OUTPUT_DIR = f"segmentation/test_multiple_seg/ground_truth_220/case_00016"

print("Loading: ", NII_IMG_PATH)

# Load the combined segmentation NIfTI file
combined_img = nib.load(NII_IMG_PATH)
combined_data = combined_img.get_fdata()

# Identify unique labels in the combined image
unique_labels = np.unique(combined_data)

print("Unique labels in the combined image:", len(unique_labels))
print("Labels:", unique_labels)


# Exclude the background label (usually 0)
unique_labels = unique_labels[unique_labels != 0]

# Extract and save individual label images
for label in unique_labels:
    # Create an empty array for the current label
    label_data = np.zeros(combined_data.shape)
    
    # Set the voxels that belong to the current label
    label_data[combined_data == label] = 1
    
    # Create a new NIfTI image for the current label
    label_img = nib.Nifti1Image(label_data, affine=combined_img.affine)
    
    # Save the label image as a new NIfTI file
    label_filename = f'label_{int(label)}.nii'
    # Create a new directory if it does not exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    nib.save(label_img, os.path.join(OUTPUT_DIR, label_filename))
    
    print(f"Label {int(label)} NIfTI file saved as '{label_filename}'")

print("All individual label NIfTI files have been saved.")
