import pickle

import numpy as np
import pandas as pd

from ..files import get_go_dir, get_model_dir
from .calculation_pipeline import calculate_pipeline_automated_one, calculate_pipeline_one


def load_model(path_to_model, path_to_keys):

    with open(path_to_model, "rb") as f:
        models = pickle.load(f)
    dsc_keys = np.genfromtxt(path_to_keys, delimiter="\n", dtype=str)
    return models, dsc_keys


def get_inference_prob_one(data, models, keys, predicted_class_label, fold=10):

    yprednogo_prob, yprednogo_cls = [], []
    rr = {}
    for k in keys:
        rr[k] = data[k]

    rr_pd = pd.Series(rr).to_frame().T

    for k in range(fold):
        curmod = models[k]
        y_pr = curmod.predict(rr_pd, prediction_type="Probability")[:, 1].copy()
        y_pr_cls = curmod.predict(rr_pd, prediction_type="Class")
        yprednogo_prob.append(y_pr)
        yprednogo_cls.append(y_pr_cls)
    yprednogo_prob = np.array(yprednogo_prob).T

    df_yprednogo = pd.DataFrame(
        data=yprednogo_prob, columns=[f"pred_llps_py92_prob_m{ii}" for ii in range(fold)], index=rr_pd.index
    )
    ynogo = np.sum(yprednogo_cls, axis=0)
    rr_pd[predicted_class_label] = ynogo
    data_ret = pd.concat([rr_pd, df_yprednogo], axis=1)
    return data_ret


def inference_model_with_go_one(fasta_dir, path_af, uniprot_id, is_automated=True):

    fold = 10
    mpath = get_model_dir()
    modelname2 = "modelpipe_depth6class1_id_2_llps_withgonocc_retrained_newgo18.sav"
    path_to_keys2 = mpath + "keys_llps_withgonocc_retrained_newgo_18.txt"

    models, keys = load_model(mpath + modelname2, path_to_keys2)

    path_files = get_go_dir()

    if is_automated:
        rr = calculate_pipeline_automated_one(path_af, uniprot_id, True, path_files)
        if rr is None:
            return -1
    else:
        rr = calculate_pipeline_one(path_af, uniprot_id, fasta_dir, True, path_files)

    dddf = get_inference_prob_one(rr, models, keys, "pred_llps_py18_go2")

    prob_columns = [f"pred_llps_py92_prob_m{ii}" for ii in range(fold)]

    dddf["pred_llps_py18_go_prob"] = np.median(dddf[prob_columns].values, axis=1)
    return dddf["pred_llps_py18_go_prob"].iloc[0]


def inference_model_without_go_one(fasta_dir, path_af, name, is_automated=True):

    fold = 10

    mpath = get_model_dir()
    modelname2 = "modelpipe_depth7class1_id_92_llps_withoutgo_24-02.sav"
    path_to_keys2 = mpath + "keys_llps_withoutgocattrue_92.txt"

    models, keys = load_model(mpath + modelname2, path_to_keys2)
    path_files = get_go_dir()
    if is_automated:
        #
        rr = calculate_pipeline_automated_one(path_af, name, False, path_files)
        if rr is None:
            return -1
    else:
        rr = calculate_pipeline_one(path_af, name, fasta_dir, False, path_files)

    dddf = get_inference_prob_one(rr, models, keys, "pred_llps_py92")
    prob_columns = [f"pred_llps_py92_prob_m{ii}" for ii in range(fold)]

    dddf["pred_llps_py92_prob"] = np.median(dddf[prob_columns].values, axis=1)
    return dddf["pred_llps_py92_prob"].iloc[0]


def pipeleine_test_one_protein():

    path_af = "../../notebooks/test_files/O95613/"
    fasta_dir = "../../notebooks/test_files/O95613/O95613.fasta.txt"
    uniprot_id = "O95613"
    path_af = "../../notebooks/test_files/Q99720/"
    fasta_dir = "../../notebooks/test_files/Q99720/Q99720.fasta.txt"
    uniprot_id = "Q99720"
    r1 = inference_model_without_go_one(fasta_dir, path_af, uniprot_id, False)
    r2 = inference_model_with_go_one(fasta_dir, path_af, uniprot_id, False)
    print(r2)  # noqa: T201
    print(r1)  # noqa: T201


def pipeleine_test_one_protein_automated():

    path_af = "../../notebooks/test_files/Q99720/"
    r1 = inference_model_without_go_one(path_af, path_af, "Q99720", True)
    print(r1)  # noqa: T201
    r2 = inference_model_with_go_one(path_af, path_af, "Q99720", True)
    print(r2)  # noqa: T201


if __name__ == "__main__":
    print("main")  # noqa: T201
