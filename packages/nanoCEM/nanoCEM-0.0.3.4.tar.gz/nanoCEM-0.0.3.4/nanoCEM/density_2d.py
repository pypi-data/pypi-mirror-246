import pandas as pd
import numpy as np
from nanoCEM.cem_utils import extract_kmer_feature
import plotnine as p9
from matplotlib import pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
from sklearn.mixture import GaussianMixture
import scipy.stats as stats
from sklearn.metrics import accuracy_score

results_path='dna_sample'
df = pd.read_csv(results_path+'/current_feature.csv')
# 创建PCA对象，并指定降维后的维度
feature,label = extract_kmer_feature(df,5,43281378)
y_test = label[0].apply(lambda x: 1 if x == 'Sample' else 0)

from statsmodels.multivariate.manova import MANOVA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
new_df = pd.DataFrame(pca.fit_transform(feature))
# import umap
# reducer = umap.UMAP(n_components=2)  # 指定降维后的维度为2
# new_df = reducer.fit_transform(feature)
new_df = pd.concat([pd.DataFrame(new_df),label], axis =1)
new_df.columns=['PC1','PC2','Group']
manova = MANOVA.from_formula('PC1 + PC2 ~ Group', data=new_df)

# 执行多元方差分析
results = manova.mv_test()

# 打印结果
print(results.summary())


plot = p9.ggplot(new_df, p9.aes(x='PC1', y='PC2',color='type'))\
    + p9.theme_bw() \
    + p9.ylim(-4,4) \
    + p9.xlim(-4,4) \
    + p9.stat_density_2d()\
    + p9.scale_color_manual(values={"Sample": "#F57070", "Control": "#9F9F9F", "Single": "#a3abbd"})\
    + p9.geom_point() \
    + p9.theme(
        figure_size=(5, 5),
        panel_grid_minor=p9.element_blank(),
        axis_text=p9.element_text(size=13),
        axis_title=p9.element_text(size=13),
        title=p9.element_text(size=13),
        legend_position='bottom',
        legend_title=p9.element_blank(),
        strip_text=p9.element_text(size=13),
        strip_background=p9.element_rect(alpha=0),
    )
plot.save(filename=results_path + "/zscore_density.pdf", dpi=300)
print(plot)

#
# plot = p9.ggplot(df, p9.aes(x='Mean',color='type'))\
#     + p9.theme_bw() \
#     + p9.geom_density() \
#     + p9.scale_color_manual(values={"Sample": "#F57070", "Control": "#9F9F9F", "Single": "#a3abbd"})\
#     + p9.theme(
#         figure_size=(5, 5),
#         panel_grid_minor=p9.element_blank(),
#         axis_text=p9.element_text(size=13),
#         axis_title=p9.element_text(size=13),
#         title=p9.element_text(size=13),
#         legend_position='bottom',
#         legend_title=p9.element_blank(),
#         strip_text=p9.element_text(size=13),
#         strip_background=p9.element_rect(alpha=0),
#     )
# plot.save(filename=results_path + "/mean_density.pdf", dpi=300)
# print(plot)

