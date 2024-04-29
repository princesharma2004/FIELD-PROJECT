"""
    AUTHOR  - Prince Sharma
    DATE    - 27/4/2024
    WORKING - laptop price predictor 
"""



import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor


def clean_memory_value(string) :
    """Helping for cleaning data from memory."""
        
    dic={"HDD" : 0, "SSD" : 0, "Hybrid" : 0, "Flash Storage" : 0}
    types = string.split("+")
    
    for i in types :
        # It is in gb or tb.
        if i.find("GB") != -1 :
            messure = "GB"
            messure_size=1
        else :
            messure = "TB"
            messure_size=1024
        
        dic[i.split(messure)[1].strip()] = int(float(i.split(messure)[0].strip())) * messure_size
        
    return [i for i in dic.values()]


class Laptop_Price_Predictor :
    """A simple class to show laptop price predictor."""
    
    
    def __init__(self) :
        """Initilize data frame."""
        
        self.df = pd.read_csv('laptop_data.csv')
    
    
    def data_clean(self) :
        """Cleaning data."""
        
        # Drop duplicates.
        self.df = self.df.drop_duplicates()
        
        # Drop unwanted columns.
        self.df.drop(columns = ["Unnamed: 0"], inplace = True)
        
        # Create company dummies and drop company.
        self.df = self.df.join(pd.get_dummies(self.df.Company))
        self.df.drop(columns = ['Company'], inplace = True)
        
        # Create typename dummies and drop typename.
        self.df = self.df.join(pd.get_dummies(self.df.TypeName))
        self.df.drop(columns = ['TypeName'], inplace = True)
        
        # Extracting data from screenresolution.
        self.df['Touchscreen'] = self.df['ScreenResolution'].apply(lambda x:True if 'Touchscreen' in x else False)
        self.df['Ips'] = self.df['ScreenResolution'].apply(lambda x:True if 'IPS' in x else False)
        self.df["ScreenResolution"] = self.df.ScreenResolution.str.split(' ').apply(lambda x : x[-1])
        self.df["Screen_Width"] = self.df.ScreenResolution.str.split('x').apply(lambda x : int(x[0]))
        self.df["Screen_Heigth"] = self.df.ScreenResolution.str.split('x').apply(lambda x : int(x[1]))
        
        # Drop screenresolution.
        self.df.drop(columns=["ScreenResolution"], inplace=True)
        
        # Cleaning ram and weight.
        self.df['Ram'] = self.df['Ram'].str.replace('GB','')
        self.df['Weight'] = self.df['Weight'].str.replace('kg','')
        
        # Converting ram and weight datatype.
        self.df['Ram'] = self.df['Ram'].astype('int64')
        self.df['Weight'] = self.df['Weight'].astype('float64')
        
        # Extracting data from cpu and drop cpu.
        self.df["CPU_Brand"] = self.df.Cpu.str.split(" ").apply(lambda x: x[0])
        self.df["CPU_Frequency"] = self.df.Cpu.str.split(" ").apply(lambda x: float(x[-1].replace("GHz",'')))
        self.df.drop(columns = ["Cpu"], inplace = True)
        
        # Extracting data from memory with the help of clean_memory_value and drop memory.
        self.df["HDD"] = self.df.Memory.apply(lambda x: clean_memory_value(x)[0])
        self.df["SSD"] = self.df.Memory.apply(lambda x: clean_memory_value(x)[1])
        self.df["Hybrid"] = self.df.Memory.apply(lambda x: clean_memory_value(x)[2])
        self.df["Flash Storage"] = self.df.Memory.apply(lambda x: clean_memory_value(x)[3])
        self.df.drop(columns = "Memory", inplace = True)
        
        # Extracting data from gpu and drop gpu.
        self.df["GPU_Brand"] = self.df.Gpu.apply(lambda x : x.split(" ")[0])
        self.df.drop(columns = "Gpu", inplace = True)
        
        # Create opsys dummies and drop opsys.
        self.df = self.df.join(pd.get_dummies(self.df.OpSys))
        self.df.drop(columns = ['OpSys'], inplace = True)
        
        # Create cpu_brand dummies with suffix _cpu and drop cpu_brand.
        cpu_categories = pd.get_dummies(self.df.CPU_Brand)
        cpu_categories.columns = [cpu + "_CPU" for cpu in cpu_categories.columns]
        self.df = self.df.join(cpu_categories)
        self.df.drop(columns = "CPU_Brand", inplace = True)
        
        # Create gpu_brand dummies with suffix _gpu and drop gpu_brand.
        gpu_categories = pd.get_dummies(self.df.GPU_Brand)
        gpu_categories.columns = [gpu + "_GPU" for gpu in gpu_categories.columns]
        self.df = self.df.join(gpu_categories)
        self.df.drop(columns = "GPU_Brand", inplace = True)
        
        # Creating pixel_per_inch column and drop screen_width , screen_height and inches column.
        self.df['ppi'] = (((self.df['Screen_Width']**2) + (self.df['Screen_Heigth']**2))**0.5 / self.df['Inches']).astype('float')
        self.df.drop(columns = ['Screen_Width', 'Screen_Heigth', 'Inches'], inplace = True)
        
        
    def train_data(self) :
        """Train data."""
        
        # Target_correlation sort by price.
        target_correlations = self.df.corr()["Price"].apply(abs).sort_values()
        
        # Chooseing Top 25 corelated features. 
        self.selected_features = target_correlations[-25:].index
        
        # Creating limited df.
        limited_df = self.df[self.selected_features]
        
        # Extracting data for traning.
        x_train, y_train = limited_df.drop(columns=["Price"]), limited_df["Price"]
        self.scaler = StandardScaler()
        x_train_scaled = self.scaler.fit_transform(x_train)
        
        # Traning model.
        self.model = RandomForestRegressor()
        self.model.fit(x_train_scaled, y_train)
        
        
    def predict(self, info) :
        test = []
        
        # Which os it is.
        op_sys = ["Chrome OS", "Windows 10", "Windows 7", "Linux", "No OS"]
        for op in op_sys :
            if op == info["op_sys"] :
                test.append(True)
            else :
                test.append(False)
                
        # It is msi or not.
        if info["brand"] == "MSI" :
            test.append(True)
        else :
            test.append(False)
            
        # Which cpu it is.
        for cpu in ['AMD', 'Intel'] :
            if cpu == info["cpu"] :
                test.append(True)
            else :
                test.append(False)
                
        # It has intel gpu or not.
        if 'Intel' == info["gpu"] :
            test.append(True)
        else :
            test.append(False)
            
        # It is touch Screen or not.
        test.append(info["touch_screen"])
        
        # It has amd gpu or not.
        if 'AMD' == info["gpu"] :
            test.append(True)
        else :
            test.append(False)
            
        # It is acer or not.
        if info["brand"] == "Acer" :
            test.append(True)
        else :
            test.append(False)
            
        # How much its weight
        test.append(info["weight"])
        
        # It is razer or not.
        if info["brand"] == 'Razer' :
            test.append(True)
        else :
            test.append(False)
            
        # It is workstation or not
        if 'Workstation' == info["type_name"] :
            test.append(True)
        else :
            test.append(False)
        
        # It is ips or not.
        test.append(info["ips"])
        
        # It is ultrabook or not
        if 'Ultrabook' == info["type_name"] :
            test.append(True)
        else :
            test.append(False)
        
        # It has nvidia gpu or not.
        if 'Nvidia' == info["gpu"] :
            test.append(True)
        else :
            test.append(False)
        
        # It is gaming or not.
        if 'Gaming' == info["type_name"] :
            test.append(True)
        else :
            test.append(False)
        
        # What is its cpu frequency.
        test.append(info["cpu_frequency"])
        
        # What is its ppi.
        test.append(((info['screen_width']**2) + (info['screen_heigth']**2))**0.5 / info['inches'])
        
        # It is notebook or not
        if 'Notebook' == info["type_name"] :
            test.append(True)
        else :
            test.append(False)
        
        # What is its ssd.
        test.append(info["ssd"])
        
        # What is its ram.
        test.append(info["ram"])
        
        x_new_scaled = self.scaler.transform([test])
        self.scaler.fit(x_new_scaled)
        
        return self.model.predict(x_new_scaled)[0]