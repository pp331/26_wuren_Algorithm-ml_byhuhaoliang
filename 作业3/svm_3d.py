from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

#准备数据 (使用鸢尾花数据集的前两个特征)
iris = datasets.load_iris()
X = iris.data[:, :2]  # 取前两个特征：花萼长度和宽度
y = iris.target       # 标签

#划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#训练 SVM 模型
model = SVC(kernel='linear', C=1.0, random_state=42)
model.fit(X_train, y_train)

#评估并直接在终端打印结果
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(" 模型基础分类准确率: {:.2f}%".format(acc * 100))
print("\n详细的分类报告：")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
print("\n 程序已顺利运行结束！")