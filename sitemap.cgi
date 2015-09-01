
__DATA__

https://www.google.com/webmasters/tools/docs/en/protocol.html

write static output to sitemap.xml(.gz)

<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
    <loc>http://www.example.com/</loc>
   <lastmod>2005-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
   </url>  
</urlset>

The Sitemap must:

    * Begin with an opening <urlset> tag and end with a closing </urlset> tag.
    * Include a <url> entry for each URL as a parent XML tag.
    * Include a <loc> child entry for each <url> parent tag. 

We require your Sitemap file to be UTF-8 encoded (you can generally do this when you save the file). As with all XML files, any data values (including URLs) must use entity escape codes for the characters listed in the table below.
Character	Escape Code
Ampersand	&	&amp;
Single Quote	'	&apos;
Double Quote	"	&quot;
Greater Than	>	&gt;
Less Than	<	&lt;

You can provide multiple Sitemap files, but each Sitemap file that you provide must have no more than 50,000 URLs and must be no larger than 10MB (10,485,760) when uncompressed. These limits help to ensure that your web server does not get bogged down serving very large files.




