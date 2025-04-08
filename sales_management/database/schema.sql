-- 门店表
CREATE TABLE IF NOT EXISTS Store (
    编号 INTEGER PRIMARY KEY AUTOINCREMENT,
    名称 TEXT NOT NULL,
    地点 TEXT,
    电话 TEXT,
    负责人 TEXT
);

-- 供货商表
CREATE TABLE IF NOT EXISTS Supplier (
    编号 INTEGER PRIMARY KEY AUTOINCREMENT,
    名称 TEXT NOT NULL,
    电话 TEXT,
    email TEXT CHECK (email LIKE '%@%')
);

-- 商品表
CREATE TABLE IF NOT EXISTS Product (
    条码 TEXT PRIMARY KEY,
    名称 TEXT NOT NULL,
    计量单位 TEXT,
    销售价格 REAL CHECK (销售价格 > 0),
    类别 TEXT CHECK (类别 IN ('食品', '服装', '图书', '电子', '日用品')) NOT NULL
);

-- 商品与供货商关联表
CREATE TABLE IF NOT EXISTS Product_and_Supplier (
    product_id TEXT NOT NULL,
    supplier_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, supplier_id),
    FOREIGN KEY (product_id) REFERENCES Product(条码),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(编号)
);

-- 图书表
CREATE TABLE IF NOT EXISTS Book (
    条码 TEXT PRIMARY KEY,
    书号 TEXT UNIQUE,
    书名 TEXT NOT NULL,
    作者 TEXT,
    定价 REAL,
    出版社 TEXT,
    出版时间 TEXT,
    版本号 TEXT,
    译者 TEXT,
    FOREIGN KEY (条码) REFERENCES Product(条码)
);

-- 客户表
CREATE TABLE IF NOT EXISTS Customer (
    联系电话 TEXT PRIMARY KEY,
    类型 TEXT CHECK (类型 IN ('会员', '非会员'))
);

-- 会员表
CREATE TABLE IF NOT EXISTS Member (
    编号 INTEGER PRIMARY KEY AUTOINCREMENT,
    姓名 TEXT NOT NULL,
    联系电话 TEXT UNIQUE NOT NULL,
    email TEXT CHECK (email LIKE '%@%'),
    地址 TEXT,
    FOREIGN KEY (联系电话) REFERENCES Customer(联系电话)
);

-- 销售记录表
CREATE TABLE IF NOT EXISTS Sale (
    单号 TEXT PRIMARY KEY,
    日期 TEXT NOT NULL,
    数量 INTEGER CHECK (数量 > 0),
    金额 INTEGER CHECK (金额 > 0),
    关联门店 INTEGER NOT NULL,
    关联商品 TEXT NOT NULL,
    关联客户 TEXT,
    FOREIGN KEY (关联门店) REFERENCES Store(编号),
    FOREIGN KEY (关联商品) REFERENCES Product(条码),
    FOREIGN KEY (关联客户) REFERENCES Customer(联系电话)
);

-- 出版社表
CREATE TABLE IF NOT EXISTS Publisher (
    编号 INTEGER PRIMARY KEY AUTOINCREMENT,
    名称 TEXT NOT NULL,
    联系电话 TEXT NOT NULL,
    联系人 TEXT,
    email TEXT CHECK (email LIKE '%@%'),
    地址 TEXT
);

-- 出版社与图书关联表
CREATE TABLE IF NOT EXISTS Publisher_and_Book (
    出版社 INTEGER NOT NULL,
    图书 TEXT NOT NULL,
    PRIMARY KEY (出版社, 图书),
    FOREIGN KEY (出版社) REFERENCES Publisher(编号),
    FOREIGN KEY (图书) REFERENCES Book(条码)
);

-- 作者表
CREATE TABLE IF NOT EXISTS Writer (
    编号 INTEGER PRIMARY KEY AUTOINCREMENT,
    笔名 TEXT
);

-- 译者表
CREATE TABLE IF NOT EXISTS Translator (
    编号 INTEGER PRIMARY KEY AUTOINCREMENT,
    笔名 TEXT
);

-- 作者与图书关联表
CREATE TABLE IF NOT EXISTS Writer_and_Book (
    writer INTEGER NOT NULL,
    book TEXT NOT NULL,
    PRIMARY KEY (writer, book),
    FOREIGN KEY (book) REFERENCES Book(条码),
    FOREIGN KEY (writer) REFERENCES Writer(编号)
);

-- 译者与图书关联表
CREATE TABLE IF NOT EXISTS Translator_and_Book (
    translator INTEGER NOT NULL,
    book TEXT NOT NULL,
    PRIMARY KEY (translator, book),
    FOREIGN KEY (book) REFERENCES Book(条码),
    FOREIGN KEY (translator) REFERENCES Translator(编号)
);