import streamlit as st
import pandas as pd
import xlrd
from io import BytesIO
import time
import chardet  # Para detectar a codificação do arquivo

def detect_encoding(uploaded_file):
    # Lê uma amostra do arquivo para detectar a codificação
    rawdata = uploaded_file.read(10000)
    uploaded_file.seek(0)  # Volta ao início do arquivo
    result = chardet.detect(rawdata)
    return result['encoding']

def main():
    st.title("Verificar dados DataImesc")
    st.write("Este app recebe um arquivo Excel e itera sobre seus registros.")
    localidades=[
    'BR', 'N', 'NE', 'SE', 'S', 'CO', 'RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO', 'MA', 
    'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA', 'MG', 'ES', 'RJ', 'SP', 'PR', 'SC', 
    'RS', 'MS', 'MT', 'GO', 'DF', '2100055', '2100105', '2100154', '2100204', '2100303', 
    '2100402', '2100436', '2100477', '2100501', '2100550', '2100600', '2100709', '2100808', 
    '2100832', '2100873', '2100907', '2100956', '2101004', '2101103', '2101202', '2101251', 
    '2101301', '2101350', '2101400', '2101509', '2101608', '2101707', '2101731', '2101772', 
    '2101806', '2101905', '2101939', '2101970', '2102002', '2102036', '2102077', '2102101', 
    '2102150', '2102200', '2102309', '2102325', '2102358', '2102374', '2102408', '2102507', 
    '2102556', '2102606', '2102705', '2102754', '2102804', '2102903', '2103000', '2103109', 
    '2103125', '2103158', '2103174', '2103208', '2103257', '2103307', '2103406', '2103505', 
    '2103554', '2103604', '2103703', '2103752', '2103802', '2103901', '2104008', '2104057', 
    '2104073', '2104081', '2104099', '2104107', '2104206', '2104305', '2104404', '2104503', 
    '2104552', '2104602', '2104628', '2104651', '2104677', '2104701', '2104800', '2104909', 
    '2105005', '2105104', '2105153', '2105203', '2105302', '2105351', '2105401', '2105427', 
    '2105450', '2105476', '2105500', '2105609', '2105658', '2105708', '2105807', '2105906', 
    '2105922', '2105948', '2105963', '2105989', '2106003', '2106102', '2106201', '2106300', 
    '2106326', '2106359', '2106375', '2106409', '2106508', '2106607', '2106631', '2106672', 
    '2106706', '2106755', '2106805', '2106904', '2107001', '2107100', '2107209', '2107258', 
    '2107308', '2107357', '2107407', '2107456', '2107506', '2107605', '2107704', '2107803', 
    '2107902', '2108009', '2108058', '2108108', '2108207', '2108256', '2108306', '2108405', 
    '2108454', '2108504', '2108603', '2108702', '2108801', '2108900', '2109007', '2109056', 
    '2109106', '2109205', '2109239', '2109270', '2109304', '2109403', '2109452', '2109502', 
    '2109551', '2109601', '2109700', '2109759', '2109809', '2109908', '2110005', '2110039', 
    '2110104', '2110203', '2110237', '2110278', '2110302', '2110401', '2110500', '2110609', 
    '2110658', '2110708', '2110807', '2110856', '2110906', '2111003', '2111029', '2111052', 
    '2111078', '2111102', '2111201', '2111250', '2111300', '2111409', '2111508', '2111532', 
    '2111573', '2111607', '2111631', '2111672', '2111706', '2111722', '2111748', '2111763', 
    '2111789', '2111805', '2111904', '2111953', '2112001', '2112100', '2112209', '2112233', 
    '2112274', '2112308', '2112407', '2112456', '2112506', '2112605', '2112704', '2112803', 
    '2112852', '2112902', '2113009', '2114007'
    ]
    def is_not_valid_number(string):
        try:
            float(string)  # Tenta converter para float (funciona para inteiros e decimais)
            return False
        except ValueError:
            return True


    uploaded_file = st.file_uploader("Carregue seu arquivo Excel", type=['csv','txt'])
   
    button=st.button("Verificar")
    if button and uploaded_file is not None:
        encoding = detect_encoding(uploaded_file)
        excel_data = pd.read_csv(uploaded_file, delimiter=';',    encoding=encoding)
            
            
        if(button):
            erros=0
            st.dataframe(excel_data)
            
            for index, row in excel_data.iterrows():
                if(row.localidade not in localidades):
                    st.write(f"Há um erro na linha {index}, a localidade {row.localidade} não está correta!")
                    erros+=1
                if(is_not_valid_number(row.value)):
                    if(row.value not in ["-","X","..."]):
                        st.write(f"Há um erro na linha {index}, o dígito {row.value} não é um digito válido!")
                        erros+=1
            if(erros==0):
                st.success("Não foram encontrados erros!")
            else:
                st.warning(f"Foram encontrados {erros} nesse arquivo")
                    
           
      
    elif button and uploaded_file is None:
        st.write("Por favor, insira a planilha.")
if __name__ == "__main__":
    main()
