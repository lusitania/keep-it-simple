<?php
if( 2 > $argc )
{
	printf( "Syntax: php %s <checkfile>.sha1\n", $argv[0] );
	exit( 1 );
}
elseif( ! file_exists( $argv[1] ) || ! ( is_file( $argv[1] ) || is_dir( $argv[1] ) ) )
{
	printf( "Error: First parameter (%s) must be a regular file or directory containing .sha1 files.", $argv[1] );
	exit( 1 );
}

$arrCheckFile	= array();
if ( is_dir($argv[1]) ){
	chdir($argv[1]);
	printf( "Changed into folder %s\n", getcwd() );
	$filesInDir	= scandir( $argv[1] );
	foreach( $filesInDir as $someFile){
		if(is_file($someFile) && fnmatch("*.sha1", $someFile))
			$arrCheckFile[]	= $someFile;
	}
}
else
	$arrCheckFile	= array( $argv[1] );

foreach( $arrCheckFile as $checksumFile )
	checkChecksums( $checksumFile );

/*
Functions
*/

function checkChecksums( $checkFile ){
	if	( false === (
		$arrCheckSumEntries	= file( $checkFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES )
		))
	{
		$err	= error_get_last();
		printf( "Error: Failed to read check sum file (%s). Reason: %s\n"
			, $checkFile
			, $err['message']
		);
	
		exit( 1 );
	}
	
	foreach( $arrCheckSumEntries as $entry )
	{
		if( false === (
			$chk_path_pair	= preg_split( "/\s+/", $entry )
		))
		{
			$err	= error_get_last();
			printf( "Error: Failed to split result %s. Reason: %s\n"
				, $entry
				, $err['message']
			);
	
			exit( 1 );
		}
	
		$chkStored	= $chk_path_pair[0];
		$path		= $chk_path_pair[1];
		
		if( ! file_exists( $path ) )
		{
			printf( "Error: I can't access %s as given in %s. Are you calling me from the correct working directory?\n"
				, $path
				, $checkFile
			);
			
			exit( 1 );
		}
		
		if( false === (
			$chkActual	= sha1_file( $path, $use_binary_encoding = false )
		))
		{
			$err	= error_get_last();
			printf( "Error: Failed to generate actual checksum for %s. Reason: %s\n"
				, $path
				, $err['message']
			);
	
			exit( 1 );
		}
		
		if( 0 !== strcmp( $chkStored, $chkActual ) )
		{
			printf( "Mismatch: %s's actual hash does not match its stored hash: %s vs. %s.\n"
				, $path
				, $chkActual
				, $chkStored
			);
			
			echo "Critical: There may be further errors. Exiting.\n";
			exit( 1 );
		}
		else
		{
			printf( "." );
		}
	}
	
	printf( "Notice: Completed %d records.\n", count( $arrCheckSumEntries ) );
}