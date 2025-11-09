data = current;

num_bins = 20;

[counts,bin_centers] = hist(current, num_bins);

bar(bin_centers, counts, 'FaceColor', [0.7 0.7 0.7], 'EdgeColor', [0.2 0.2 0.2]);
hold on;

% Fit a Gaussian distribution
pd = fitdist(current, 'Normal');

% Generate values for the Gaussian fit
x = linspace(min(current), max(current), 100);
y = pdf(pd, x) * length(current) * (bin_centers(2) - bin_centers(1));

% Plot the Gaussian fit
plot(x, y, 'r-', 'LineWidth', 2);

% Add labels and title
xlabel('Histogram');
ylabel('Number of samples');
title('Histogram of Current with Gaussian Fit');

% Calculate mean and standard deviation
mean_current = mean(current);
std_current = std(current);

fprintf('Mean of current: %.4f\n', mean_current)
fprintf('Standard Deviation of current: %.4f\n', std_current)
