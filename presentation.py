"""
Code for preparing presentation stuff.
"""
import matplotlib
matplotlib.use('Agg')
import os
import re
import imageio as imageio
import numpy as np
import shutil
import matplotlib.pyplot as plt
from scipy.stats import norm, gamma, uniform
import seaborn as sns
import matplotlib2tikz

from utility import MixtureModel

sns.set()
dpi = 300


def generate_data_concept_images():
    np.random.seed(4)
    sns.set_style('dark')
    figure, axes = plt.subplots(dpi=dpi)
    x_axis = np.arange(-6, 6, 0.001)
    mixture_model = MixtureModel([norm(-3, 1), norm(3, 1)])
    mean_samples = mixture_model.rvs(3)
    axes.plot([mean_samples[0], mean_samples[0]], [0, mixture_model.pdf(mean_samples[0], 0, 1)], color=sns.color_palette()[1])
    axes.plot([mean_samples[1], mean_samples[1]], [0, mixture_model.pdf(mean_samples[1], 0, 1)], color=sns.color_palette()[2])
    axes.plot([mean_samples[2], mean_samples[2]], [0, mixture_model.pdf(mean_samples[2], 0, 1)], color=sns.color_palette()[4])
    axes.plot(x_axis, mixture_model.pdf(x_axis), color=sns.color_palette()[0])
    plt.savefig('mean_generating_distribution.png', dpi=dpi)
    plt.close(figure)

    figure, axes = plt.subplots(dpi=dpi)
    x_axis = np.arange(0, 6, 0.001)
    gamma_distribution = gamma(2)
    std_samples = gamma_distribution.rvs(3)
    axes.plot([std_samples[0], std_samples[0]], [0, gamma_distribution.pdf(std_samples[0])], color=sns.color_palette()[1])
    axes.plot([std_samples[1], std_samples[1]], [0, gamma_distribution.pdf(std_samples[1])], color=sns.color_palette()[2])
    axes.plot([std_samples[2], std_samples[2]], [0, gamma_distribution.pdf(std_samples[2])], color=sns.color_palette()[4])
    axes.plot(x_axis, gamma.pdf(x_axis, 2), color=sns.color_palette()[0])
    plt.savefig('std_generating_distribution.png', dpi=dpi)
    plt.close(figure)

    figure, axes = plt.subplots(dpi=dpi)
    minimums = mean_samples - (3 * std_samples)
    maximums = mean_samples + (3 * std_samples)
    minimum = np.min(minimums)
    maximum = np.max(maximums)
    x_axis = np.arange(minimum, maximum, 0.001)
    example_norms = [norm(mean_samples[0], std_samples[0]), norm(mean_samples[1], std_samples[1]), norm(mean_samples[2], std_samples[2])]
    axes.plot(x_axis, example_norms[0].pdf(x_axis), color=sns.color_palette()[1])
    axes.plot(x_axis, example_norms[1].pdf(x_axis), color=sns.color_palette()[2])
    axes.plot(x_axis, example_norms[2].pdf(x_axis), color=sns.color_palette()[4])
    axes.set_ylim(0, 0.3)
    plt.savefig('example_normals.png', dpi=dpi)
    plt.close(figure)

    figure, axes = plt.subplots(dpi=dpi)
    x_axis = np.arange(mean_samples[0]-5, mean_samples[0]+5, 0.001)
    observations = example_norms[0].rvs(10)
    observation_color = sns.xkcd_rgb['medium grey']
    print(np.round(observations, 3))
    for observation in observations:
        axes.plot([observation, observation], [0, example_norms[0].pdf(observation)], color=observation_color)
    axes.plot(x_axis, example_norms[0].pdf(x_axis), color=sns.color_palette()[1])
    plt.savefig('normal_with_observations.png', dpi=dpi)
    plt.close(figure)


def generate_polynomial_concept_images():
    np.random.seed(0)
    sns.set_style('darkgrid')
    figure, axes = plt.subplots(dpi=dpi)
    x_axis = np.arange(-1, 1, 0.001)
    axes.plot(x_axis, (-1 * (x_axis ** 4)) + (-1 * (x_axis ** 3)) + (2 * (x_axis ** 2)) + x_axis, color=sns.color_palette()[4])
    observation_color = sns.xkcd_rgb['medium grey']
    for observation in np.linspace(-1, 1, num=10):
        axes.plot([observation, observation], [0, -1 * observation ** 4 + -1 * observation ** 3 + 2 * observation ** 2 + observation], color=observation_color)
    plt.savefig('polynomial_with_observations.png', dpi=dpi)
    matplotlib2tikz.save(os.path.join('latex', 'polynomial_example.tex'))
    plt.close(figure)


def generate_single_peak_double_peak(mean_offset=3):
    sns.set_style('darkgrid')
    figure, axes = plt.subplots(dpi=dpi)
    x_axis = np.arange(-5, 5, 0.001)
    axes.plot(x_axis, norm(0, 1).pdf(x_axis), color=sns.color_palette()[0])
    axes.plot(x_axis, MixtureModel([norm(-mean_offset, 1), norm(mean_offset, 1)]).pdf(x_axis), color=sns.color_palette()[1], label='HHZ 1')
    matplotlib2tikz.save(os.path.join('latex', 'single_peak_double_peak.tex'))
    plt.show()
    plt.close(figure)


def generate_display_frame(trial_directory, fake_examples, unlabeled_predictions, test_predictions, dnn_test_predictions, train_predictions, dnn_train_predictions, step):
    sns.set_style('darkgrid')
    bandwidth = 0.1
    fake_a3 = np.transpose(np.polyfit(np.linspace(-1, 1, num=10), np.transpose(fake_examples[:, :10]), 3))
    x_axis_limits = [-4, 4]
    x_axis = np.arange(*x_axis_limits, 0.001)
    figure, axes = plt.subplots(dpi=dpi)
    axes.text(0.98, 0.98, 'Step: {}'.format(step), horizontalalignment='right', verticalalignment='top', family='monospace', fontsize=10, transform=axes.transAxes)
    axes.plot(x_axis, MixtureModel([uniform(-1, 2)]).pdf(x_axis), color=sns.color_palette()[0], label='Real Data Distribution')
    try:
        axes = sns.kdeplot(fake_a3[0, :], ax=axes, color=sns.color_palette()[4], bw=bandwidth, label='Fake Data Distribution')
    except ValueError:
        pass
    axes = sns.kdeplot(unlabeled_predictions, ax=axes, color=sns.color_palette()[1], bw=bandwidth, label='Unlabeled Predictions')
    axes = sns.kdeplot(test_predictions, ax=axes, color=sns.color_palette()[2], bw=bandwidth, label='GAN Test Predictions')
    axes = sns.kdeplot(train_predictions, ax=axes, color=sns.color_palette()[2], linewidth=0.5, bw=bandwidth, label='GAN Train Predictions')
    axes = sns.kdeplot(dnn_test_predictions, ax=axes, color=sns.color_palette()[3], bw=bandwidth, label='DNN Test Predictions')
    axes = sns.kdeplot(dnn_train_predictions, ax=axes, color=sns.color_palette()[3], linewidth=0.5, bw=bandwidth, label='DNN Train Predictions')
    axes.set_xlim(*x_axis_limits)
    axes.set_ylim(0, 1)
    axes.legend(loc='upper left')
    figure.tight_layout(pad=0)
    figure.canvas.draw()
    image_array = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    image_array = image_array.reshape(figure.canvas.get_width_height()[::-1] + (3,))
    plt.close(figure)
    return image_array
    # plt.savefig(os.path.join(trial_directory, '{}/{}.png'.format(settings.temporary_directory, step)), dpi=dpi, ax=axes)
    # plt.close(figure)
    # return imageio.imread(os.path.join(trial_directory, '{}/{}.png'.format(settings.temporary_directory, step)))


def natural_sort_key(string, natural_sort_regex=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(natural_sort_regex, string)]


def generate_video_from_frames(trial_directory, settings):
    fps = 20
    file_names = [file for file in os.listdir(os.path.join(trial_directory, settings.temporary_directory)) if file.endswith('.png')]
    file_names.sort(key=natural_sort_key)
    video_writer = imageio.get_writer(os.path.join(trial_directory, '{}.mp4'.format(os.path.basename(trial_directory))), fps=fps)
    for file_name in file_names:
        image = imageio.imread(os.path.join(trial_directory, '{}/{}'.format(settings.temporary_directory, file_name)))
        video_writer.append_data(image)
    video_writer.close()
    shutil.rmtree(os.path.join(trial_directory, settings.temporary_directory))
    print('\nMeans Video Complete.')


def generate_dnn_vs_gan_average_per_number_of_examples():
    dnn_results = {15: [0.3970],
                   30: [0.3393],
                   100: [0.0883],
                   300: [0.0721],
                   1000: [0.0545]}
    gan_results = {15: [0.2067],
                   30: [0.1975],
                   100: [0.0827],
                   300: [0.0711],
                   1000: [0.0543]}
    average_dnn_results = {example_count: np.mean(values) for example_count, values in dnn_results.items()}
    average_gan_results = {example_count: np.mean(values) for example_count, values in gan_results.items()}
    dnn_plot_x, dnn_plot_y = zip(*sorted(average_dnn_results.items()))
    gan_plot_x, gan_plot_y = zip(*sorted(average_gan_results.items()))
    dnn_plot_y, gan_plot_y = np.array(dnn_plot_y), np.array(gan_plot_y)
    figure, axes = plt.subplots(dpi=dpi)
    axes.set_xscale('log')
    axes.set_xticks(dnn_plot_x)
    axes.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axes.set_yscale('log')
    axes.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axes.get_yaxis().set_minor_formatter(matplotlib.ticker.ScalarFormatter())
    axes.plot(dnn_plot_x, dnn_plot_y, color=sns.color_palette()[3], label='DNN')
    axes.plot(gan_plot_x, gan_plot_y, color=sns.color_palette()[2], label='GAN')
    axes.set_xlabel('Labeled Dataset Size')
    axes.set_ylabel('Coefficient MAE')
    axes.legend().set_visible(True)
    matplotlib2tikz.save(os.path.join('latex', 'coefficient-gan-vs-dnn.tex'))
    plt.show()
    plt.close(figure)
    figure, axes = plt.subplots()
    axes.set_xscale('log')
    axes.set_xticks(dnn_plot_x)
    axes.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axes.set_xlabel('Labeled Dataset Size')
    axes.set_ylabel('GAN to DNN Relative Error')
    axes.plot(gan_plot_x, gan_plot_y / dnn_plot_y, color=sns.color_palette()[2])
    matplotlib2tikz.save(os.path.join('latex', 'coefficient-gan-to-dnn-relative-error.tex'))
    plt.show()
    plt.close(figure)


def nash_equilibrium_plot():
    figure, axes = plt.subplots(dpi=dpi)
    points = np.array([(1, 0), (0, -1), (-1, 0), (0, 1), (1, 0)])
    axes.plot(*zip(*points), color=sns.color_palette()[0], label='DNN')
    matplotlib2tikz.save(os.path.join('latex', 'nash_equilibrium.tex'))
    #plt.savefig('nash_equilibrium.png', dpi=dpi, ax=axes, transparent=True)
    plt.show()
    plt.close(figure)

if __name__ == '__main__':
    plt.switch_backend('module://backend_interagg')
    nash_equilibrium_plot()
