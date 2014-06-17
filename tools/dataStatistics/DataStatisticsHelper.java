import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;


/*	
Class that takes in the csv generated from dataStatistics.py
and generates a new csv with all the statistical properties.

USAGE :
java DataStatisticsHelper inputCSVFile [MAX_THREADS = 4]

*/
public class DataStatisticsHelper
{
	private static BufferedWriter bw;
	
	private class ChannelRecord
	{
		private String channel;
		private float frequency;
		private double values[];
		private boolean seizure;

		private double sum, sumOfSquares, minVal, maxVal;
		private long countValues;
		
		private double median;

		public ChannelRecord(String row) throws Exception
		{
			Scanner scan = new Scanner(row);
			scan.useDelimiter(",");
			
			try{
				frequency = scan.nextFloat();
			}
			catch(Exception e)
			{
				scan.close();
				throw new Exception("Unable to process row : Failed at frequency", e);
			}
			try{
				if(scan.next().equals("interictal"))
					seizure = false;
				else
					seizure = true;
			}catch(Exception e)
			{
				scan.close();
				throw new Exception("Unable to process row : Failed at seizure state", e);
			}

			try{
				channel = scan.next();
			}catch(Exception e)
			{
				scan.close();
				throw new Exception("Unable to process row : Failed at channel", e);
			}
			
			ArrayList<Double> valuesList = new ArrayList<Double>();;
			try{
				while(scan.hasNext())
					valuesList.add(scan.nextDouble());
			}
			catch(Exception e)
			{
				scan.close();
				throw new Exception("Unable to process row : Failed at populating values", e);
			}
			
			scan.close();
			
			sum = 0;
			sumOfSquares = 0;
			
			values = new double[valuesList.size()];
			minVal = Double.MAX_VALUE;
			maxVal = Double.MIN_VALUE;
			int index = 0;
			for(double value : valuesList)
			{
				values[index++] = value;
				sum+=value;
				sumOfSquares += (value*value);
				
				maxVal = value > maxVal ? value : maxVal;
				minVal = value < minVal ? value : minVal;
			}
			
			countValues = values.length;
			//System.out.println("Number of values = " + countValues);
			median = Double.MIN_VALUE;
		}
		
		public double getMinValue()
		{
			//System.out.println("Finding Min Value");
			return minVal;
		}

		public double getMaxValue()
		{
			//System.out.println("Finding Max Value");
			return maxVal;
		}
		
		public double getVariance()
		{
			//System.out.println("Finding Variance");
			double mean = getMean();
			return ((Math.pow(mean, 2)*countValues) + sumOfSquares - (2*mean*sum))/(countValues-1);
		}

		public double getStdDev()
		{
			//System.out.println("Finding Standard deviation");
			return Math.sqrt(getVariance());
		}

		public double getMean()
		{
			//System.out.println("Finding Average");
			return sum/countValues;
		}

		public double getMedian()
		{
			//System.out.println("Finding Median");
			if(median != Double.MIN_VALUE)
				return median;
			
			double valuesCopy[] = Arrays.copyOf(values, values.length);
			Arrays.sort(valuesCopy);
			median = valuesCopy[valuesCopy.length/2];
			return median;
		}
		
		@Override
		public String toString()
		{
			return frequency+","
					+channel+","
					+seizure+","
					+getMinValue()+","
					+getMaxValue()+","
					+getMean()+","
					+getVariance()+","
					+getStdDev()+","
					+getMedian()+"\r\n";
		}
	}
	
	public static void main(String args[]) throws IOException, Exception 
	{
		DataStatisticsHelper object = new DataStatisticsHelper();
		if(args.length == 0 )
		{
			System.out.println("Please provide source data file");
			System.out.println("USAGE : java DataStaisticsHelper CSVFilename maxThreads");
		}
		
		String dataFile = args[0];
		
		int MAX_THREADS = 4;
		if(args.length == 2)
			MAX_THREADS = Integer.parseInt(args[1]);
		
		FileReader reader = null;
		try{
			reader = new FileReader(new File(dataFile));
		}catch(FileNotFoundException e)
		{
			System.out.println("The source file does not exist.");
			System.exit(1);
		}
		BufferedReader br = new BufferedReader(reader);
		
		FileWriter write = new FileWriter(new File(dataFile.substring(0,dataFile.length()-4) + "_stats.csv"));
		bw = new BufferedWriter(write);
		
		bw.write("Frequency,Channel,Seizure State,Min Value, Max Value,Mean,Variance,Standard Deviation,Median\r\n");
		bw.flush();
		
		String row;
		int rowCount=1;
		
		AnalysisThread threadArray[] = new AnalysisThread[MAX_THREADS];
		
		while((row = br.readLine()) != null)
		{
			int threadCount = 0;
			for( ; threadCount < MAX_THREADS && row != null ; threadCount++)
			{
				System.out.println("**************  PROCESSING ROW "+rowCount+"  ********************");
				threadArray[threadCount] = object.new AnalysisThread(row, object);
				if( threadCount != MAX_THREADS - 1 )
					row = br.readLine();
				rowCount++;
			}
			
			for( int i = 0; i < threadCount ; i++)
			{
				threadArray[i].start();
			}
			
			for( int i = 0; i < threadCount ; i++)
			{
				threadArray[i].join();
			}
		}
		bw.flush();
		bw.close();
		write.close();
		br.close();
		reader.close();
	}
	
	private class AnalysisThread extends Thread //implements Callable<String>
	{
		String row;
		DataStatisticsHelper object;
		String result;
		
		public AnalysisThread(String row,DataStatisticsHelper object) {
			this.row = row;
			this.object = object;
		}
		
		public void run()
		{
			ChannelRecord record;
			try {
				record = object.new ChannelRecord(row);
				result = record.toString();
				synchronized (bw) {
					System.out.println("Writing to file");
					bw.write(result);
					bw.flush();
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}