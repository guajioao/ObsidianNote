# Java基础概念
#### JDK(Java Development Kit Java开发者工具包)
必须安装JDK才能使用Java
* LTS版本：JDK8（\*）,JDK11（\*）,JDK17,JDK21
* JDK组成
![[Pasted image 20250611150526.png]]
#### IDEA快捷键
![[Pasted image 20250611151921.png]]
#### Java数据
* 范围与内存占用：![[Pasted image 20250611153213.png]]
* 范围小的变量可以直接赋值给类型范围大的变量
	* ![[Pasted image 20250611153941.png]]
* 范围大的变量转范围小的变量->**强制类型转换**【不强制转换会报错】
```
int i=20;
byte j = (byte)i; //20在byte类型范围内，因此j=20
i=1500;
j = (byte)i; //1500不在byte类型范围内，因此j=-35，数据溢出
```
* 浮点型转成整数，直接去掉小数部分
* 表达式的最终类型由表达式中的最高数据类型决定：
	* 例如：1+1.0=2.0；10/3=3【小数被人扔了】
* 在表达式中，byte、short、char 是**直接转换成int**类型参与运算的。(byte)a+(byte)b=(int)c
#### 标识符
1.以字母(a-z,A-Z)，美元符号(**$**)，或者下划线(\_)开始。**数字不能**作为标识符的开头。
2.后续可以包含字母、数字(0-9)、美元符号($)或下划线(\_)
3.区分大小写，myVariable 和 MyVariable 是两个不同的标识符。
4.不能与Java中的关键字重名
5.应遵循驼峰命名法，即变量名和方法名**首字母小写**，后续每个单词首字母大写;类名首字母大写，后续每个单词首字母大写。


#### 运算符
* +从前往后，能加则加，不能加则连接
	* "abc" + 5 = "abc5"
	* 5+'a' +"abc"="102abc"
* 自增，自减符++，--
```
int a=10;
int res = ++a; //先加再用，res=11,a=11
int a=10;
int res = a++; //先用再加，res=10,a=11
```
* 关系运算符
	* ![[Pasted image 20250611160241.png]]
* 三元运算符： 条件表达式?值1:值2;
```
	int max = a>b ? a:b;
```
* 逻辑运算符
	* ![[Pasted image 20250611160631.png]]
	* 双与、双或：只要左边为false，右边就不执行了![[Pasted image 20250611160801.png]]
#### Switch
* Switch的穿透性
	* 如果没有break，则后续都会执行
```
public static void test3(){ 
	String week="周二"
	switch(week){
		case"周一":
			System.out.println("埋头苦干，决bug");
			break;
		case"周二": //穿透，继续向下
		case"周三": //穿透，继续向下
		case"周四": //遇到break，停止
			System.out.println("请求大牛程序员帮忙");
			break;
		case"周五":
			System.out.println("自己整理代码”);
			break;
		case"周六":
		case"周日":
			System.out.println("打游戏");
			break;
		default:
			System.out.println("星期信息有误!");
	}
	// 输出:
	请求大牛程序员帮忙
	请求大牛程序员帮忙
	请求大牛程序员帮忙
}
```
#### 数组
* 一维数组初始化
```
int[] s = {1, 2, 3}; //静态初始化
double[] s = new double[8]; //动态初始化
```
* 二维数组初始化
```
int[][] s = new int[][]{{1, 2}, {3}, {5, 6, 7}}; //静态初始化
double[] s = new double[8][5]; //动态初始化
```
#### 方法
* 方法**重载**：方法名相同，形参列表不同

#### 对象
**程序的调用过程**：
* 方法区：存放Class
* 栈内存：
	* 存放方法，先进后出；
	* 变量存在栈中，指向堆中的对象
* 堆内存：
	* new出的对象放在堆中
	* 对象中包含类的地址，调用对象的方法时通过将类的方法调到栈中来执行
**面向对象的三大特征：封装、继承、多态**
#### 类Class
* 成分：
	* 构造器：不能写返回值类型，名称必须是类名【初始化new一个类时调用】
		* 创建对象时会自动调用构造器，完成初始化赋值
		* 类默认自带一个无参构造器，但当自定义有参构造器后默认的无参构造器就没有了，还需要的话必须自定义一个无参构造器
* this关键字
	* 可以用在方法中，来拿到当前的对象
```
String cont = "name";  
public String getCont(String cont) {  
	return this.cont + "and" + cont;  //通过this来区分对象本身的变量与传入的参数
}
```
* 封装
	* 类就是一种封装
	* 设计要求：合理隐藏，合理暴露
	```
	public class Student{  
	    private String name;  
	    private String psw;  
	  
	    public void setName(String name) {  
		    // *** 一些校验
	        this.name = name;  
	    }  
	  
	    public String getName() {  
	        return name;  
	    }  
	  
	    public void setPsw(String psw) {  
		    // *** 一些校验
	        this.psw = psw;  
	    }  
	  
	    public String getPsw() {  
	        return psw;  
	    }  
	}
	```
* JavaBean
	* 成员变量全部私有，提供get/set方法
	* 需要一个无参构造器，有参构造器可选
* **static关键字**
	* 静态变量：属于类，所有的对象共享这个静态变量
		* 在**堆内存**中开劈一块区域存储该静态变量的值
	* 实例变量：无static，属于每个对象
	* 静态方法中可以直接访问静态成员，**不可以**直接访问实例成员。
	* 实例方法中既可以直接访问静态成员，也可以直接访问实例成员
	* 实例方法中可以出现this关键字，静态方法中**不可以**出现this关键字的。
	* 示例
		* ![[Pasted image 20250611170146.png]]
	```
	public class Student{  
	    static String name="111";  //静态变量
		String psw;  // 实例变量
		public static void getName(){ 
			//静态方法可以直接访问静态变量name，不可以访问psw
			System.out.println(name);
		}
	}
	// 可以直接使用Student.name来获得变量值
	Student.name = "222";
	// 也可以用对象名来访问，但多个对象进行修改后以最后一个修改的为最终值
	Student s1 = new Student();
	Student s2 = new Student();
	s1.name = "333"; // Student.name = s1.name = s2.name="333"
	s2.name = "444"; // Student.name = s1.name = s2.name="444"
	//
	```
* **继承extends**
	* 优势：提高代码重用性
	* 子类可以继承父类的非私有成员(成员变量、成员方法)
		* 单继承，只能有一个父类，但可以多层继承
		* java中所有类都是Object类的子类
		* 就近原则，优先访问自己的成员，没有才会访问父类；
		* 如果指定要访问父类，可以使用**super关键字**
	* 方法重写
	* 子类构造器：
		* 先调用父类构造器，再调用自己的
		* 默认第一行都是super();如果父类没有无参构造器，则必须手写super(...)指定调用父类的有参构造器
		* 可以在第一行用this(...)调用兄弟构造器。但不能与super();同时出现【不然会多次调用super():】
			```
				public class Student{  
				    private String name;  
				    private String psw; 
				    public Student(){} 
				    public Student(String name){
					    this.name = name;
				    } 
				    public Student(String name,String psw){
					    super(name);
					    this.psw=psw;
				    } 
			```
* 权限修饰符
	* private：只能本类
	* 缺省：本类、同一个包中的类【没有这些权限修饰符】
	* protected：本类、同一个包中的类、子孙类
	* public：任何位置
* **多态**
	* 在继承/实现情况下的一种现象，表现为：对象多态、行为多态
	* 示例：``` Animal a = new Wolf(); ```
	* 此时a.name依然是Animal类的初始化，不是Wolf的，因为成员变量不在多态范围内
	* 问题：
		* 多态不能使用子类的独有功能
			``` 
			Animal a = new Wolf(); 
			// a.eatSheep();会报错，因为eatSheep是狼独有的方法
			```
	* 类型转换问题：
		* 自动转换：父类 变量名= new 子类();
		* 强制类型转换：子类 变量名 = (子类)父类变量()		
			```
			Animal a = new Wolf(); 
			Wolf b = (Wolf)a; 
			a.eatSheep();// 不报错了，因为eatSheep是狼独有的方法
			// Sheep c = (Sheep)a; 报错，因为a的真是类型不是Sheep
			// 可以使用instanceof关键字判断真实类型
			if(a instanceof Sheep){
				Sheep c = (Sheep)a;//如果真实类型符合才会进来
			}
			```
