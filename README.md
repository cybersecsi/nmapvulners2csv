# nmapvulners2csv
Convert Nmap vulners script output to CSV

## Table of Contents
- [Getting Started](#getting-started)
  - [Install](#install)
  - [Run without installing](#run-without-installing)
    - [Prerequisites](#prerequisites)
  - [Evidences Description](#evidences-description)
- [Contributing](#contributing)
- [License](#license)

## Getting Started  
Run nmap with enabled script Vulners and save xml output, for example:   
```  
nmap -sV --script vulners -oX <nmap_output.xml>  
```  

### Install
To install it you just need to run:
```
pip install nmapvulners2csv
```

### Run without installing

#### Prerequisites   
Install dependencies by using the following command:   
``` 
pip install -r requirements.txt
```

```   
Usage: nmapvulners2csv.py NMAP_XML_FILE <flags>
  optional flags:        --output | --descr
  
```  

To run the converter:   
```  
python nmapvulners2csv <nmap_output.xml>   
``` 

the script will generate a file output.csv in output dir. If you want to set the output file:   
```   
python nmapvulners2csv <nmap_output.xml>  --output <output_csv_file> --dir <output_directory>
``` 
For multiple data:   
```  
for i in `ls -1 vulners*`; do python nmapvulners2csv.py $i ${i%%.xml}.csv ; done   
``` 

### Evidences Description  
``nmapvulners2csv`` does not generate descriptions for vulnerabilities. You can add `--descr` flag to add descriptions in CSV.  The script scrapes description information from Vulners site. The command is more time-expensive and send several HTTP requests against Vulners website. Not tested for IP ban and network issues.     

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under Apache 2 License. See `LICENSE` for more information. 