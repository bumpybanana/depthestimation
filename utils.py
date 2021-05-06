import torch
import torchvision
from dataset import DepthDataset
from torch.utils.data import DataLoader

def save_checkpoint(state,filename="my_checkpoint.pth.tar"):
    print("Saving checkpoint")
    torch.save(state,filename)

def load_checkpoint(checkpoint,model):
    print("Loading checkpoint")
    model.load_state_dict(checkpoint["state_dict"])

def get_loaders(
        train_rgb_folder,
        train_depth_folder,
        test_rgb_folder,
        test_depth_folder,
        batch_size,
        transformation,
        num_workers=1,
        pin_memory=True,
):
    train_dataset = DepthDataset(
        rgb_dir=train_rgb_folder,
        depth_dir=train_depth_folder,
        transform=transformation,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=True,
    )

    test_dataset = DepthDataset(
        rgb_dir=test_rgb_folder,
        depth_dir=test_depth_folder,
        transform=transformation
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=False,
    )

    return train_loader, test_loader

def check_accuracy(loader, model, device="cuda"):
    num_correct = 0
    num_pixels = 0
    model.eval()

    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device)
            preds = torch.sigmoid(model(x))
            num_correct += (preds == y).sum()
            num_pixels += torch.numel(preds)

    print(f"Got{num_correct}/{num_pixels} with acc {num_correct/num_pixels*100:.2f}")

    model.train()

def save_predictions_as_imgs3x3(
        loader, model, folder ="saved_images3x3/",device="cuda"
):
    model.eval()
    for index, (x, y) in enumerate(loader):
        x = x.to(device=device)
        with torch.no_grad():
            preds = torch.sigmoid(model(x))
        torchvision.utils.save_image(
            preds, f"{folder}/pred_{index}.png"
        )
        torchvision.utils.save_image(y,f"{folder}{index}.png")

    model.train()

def save_predictions_as_imgs7x7(
        loader, model, folder ="saved_images7x7/",device="cuda"
):
    model.eval()
    for index, (x, y) in enumerate(loader):
        x = x.to(device=device)
        with torch.no_grad():
            preds = torch.sigmoid(model(x))
        torchvision.utils.save_image(
            preds, f"{folder}/pred_{index}.png"
        )
        torchvision.utils.save_image(y,f"{folder}{index}.png")

    model.train()

def save_predictions_as_imgs_squeeze(
        loader, model, folder ="saved_images_squeeze/",device="cuda"
):
    model.eval()
    for index, (x, y) in enumerate(loader):
        x = x.to(device=device)
        with torch.no_grad():
            preds = torch.sigmoid(model(x))
        torchvision.utils.save_image(
            preds, f"{folder}/pred_{index}.png"
        )
        torchvision.utils.save_image(y,f"{folder}{index}.png")

    model.train()



