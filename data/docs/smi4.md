---


# LEGS: Library of Engineering Graphics Software


			  SUN Microsystems, Inc.
			    2310 Walsh Avenue
			  Santa Clara, CA 95051

			    July 3, 1982

			   **PRELIMINARY**


>

**Abstract**
SUN offers a comprehensive package of engineering graphics software
which provides the underlying support required for interactive graphics
applications programs.	The LEGS software is an implementation of the ACM
CORE graphics specification plus extensions.  The CORE is implemented for basic
two-dimensional and three-dimensional operations with segmentation.
Extensions to the CORE include textured polygon fill algorithms, quadratic
and cubic curve drawing, extended vector and matrix operations,
shaded surface polygon rendering and bicubic patch drawing with selectable
texture mapping and hidden surface elimination.

This graphics package supports both the high resolution monochrome bit map
display and the SUN color display.  Device dependant routines support
both of these displays under the LEGS package.

This document is a list of the functions available.


**Keywords:** CORE Graphics Standard, Graphics Library,
Vector, Polygon, Splines, Texture, RasterOp


>

The information contained in this document is subject to change
without notice and should not be construed as a committment
by SUN Microsystems, Inc. SUN Microsystems Inc
assumes no responsibility for errors that may appear in this document.

The software programs described in this document are confidential
information and proprietary product of SUN Microsystems Inc.


---


**Input routines**

User interactive devices on the SUN include the keyboard
with special function keys and a mouse driven cursor.  The mouse has
three buttons in addition to its (x,y) positioning capability.


```

inq$button(&buttons)		read mouse switches
wait$button(&button)		await mouse button
init$locator(onoff)		turn cursor on or off
inq$locator(&x,&y)		get cursor position
set$locator(x,y)		set cursor position
init$keyboard()			set up keyboard for polling
inq$key(&char)			see if key has been hit
wait$key(&char)			await key hit

```


**Line routines**

These routines draw vectors and curves on the SUN bitmap graphics
display.  The Bresenham algorithm is used for all vectors except
horizontal and vertical lines.	These lines are drawn using more
efficient transfers to the hardware.  Attributes of the line may
be specified with additional calls.


```

lin$intens(intens)		set line color
lin$width(width)		set line width
lin$style(style)		set line style
lin$mode(mode)			set transform mode
mov2$abs(x,y)			move to framebuf location (x,y)
drw2$abs(x,y)			draw to framebuf location (x,y)
mov2$rel(dx,dy)			move relative to current location
drw2$rel(dx,dy)			draw relative to current location
pll2$abs(xarray,yarray,n)	draw n connected line segments
				in absolute framebuffer coordinates
pll2$rel(dxarray,dyarray,n)	draw n connected line segments
				in relative steps
curv2$abs(x,y,dx1,dy1,dx2,dy2)	draw curve from current 2-D point to
				(x,y) with starting tangent (dx1,dy1)
				and ending tangent (dx2,dy2)
mov3$abs(x,y,z)			move to absolute 3-D location
drw3$abs(x,y,z)			draw to absolute 3-D location
mov3$rel(dx,dy,dz)		move relative to 3-D location
drw3$rel(dx,dy,dz)		draw relative to 3-D location
curv3$abs(x,y,z,dx1,dy1,dz1,dx2,dy2,dz2)
				draw curve from current 3-D point to
				(x,y,z) with start and end tangents
				(dx,dy,dz)
splin2$abs(x2,y2,x0,y0,x3,y3)	2-D cubic spline from current point to
				P2
splin3$abs(x2,y2,z2,x0,y0,z0,x3,y3,z3)
				cubic spline from current point to P2

```


**Patch routines**

These routines draw bicubic patches on a display device.  The
patch may be displayed as wire mesh, or smooth shaded with optional
mapping of imagery and/or texture on the surface.  Hidden surfaces
are eliminated via the disk paged z-buffer if the hidden attribute
is specified.  For shading, the Catmull subdivision algorithm is used
with subdivision of patch coordinates and normal vectors.  Texture
and image mapping is done from disk files which hold the image and the
array of normal dithers which define the texture surface.


```

pat$style(style)		set patch drawing style
pat$image(image$id)		set image map file id number
pat$texture(texture$id)		set texture map file id number
pat$color(color)		set patch color
drw$patch(ctl$pts)		draw patch from control points

```


**Polygon routines**

These routines fill regions and plot polygons in 2 or 3 dimensions.
Region filling is done either within a boundary of a given color or
within a boundary specified as a list of vector edges.	Scan line
coherence is fully utilized in a sophisticated algorithm for efficient
region filling.  Polygons may be plotted as vector outlines, constant
shaded, Gouraud shaded, or Phong shaded.  For 3-D operations the polygons
are transformed and clipped according to the current transformation
and viewport.  For hidden surface removal a paged disk file z-buffer is
used which is the same size as the viewport.


```

ld$texture(txtptr, txtfunc)	load 16 word texture pattern
pol$texture(texture)		set texture for region fill
bound$fill(x, y, oldval, newval)
				fill region within drawn bounds
				starting at interior point x,y
region(xlist, ylins, npts)	fill region defined by vector list
polygon(xlist, ylist, zlist, npts)
				plot planar convex region

```


**Raster routines**

These routines move and modify rectangular raster areas which reside
in the framebuffer, the colorbuffer, or in memory.  Rasters
are clipped to the current view port.


```

ras$dev(device)			set device$id
ras$copy(xs, ys, h, w, xd, yd, func)
				short xs,ys,xd,yd:
				source and destination locations
				in framebuffer coordinates;
				short h,w,func:
				height, width and function
ras$get(x,y,h,w,buf,func)	copy from frame buffer to memory
ras$put(x,y,h,w,buf,func)	copy from memory to frame buffer
ras$write(w,h,x,y)		write a raster rectangle
ras$line(w,x,y)			write a line segment to the framebuffer
ras$clear()			zero the entire screen

```


**Text routines**

These routines provide for plotting characters on the SUN graphics
display in two or three dimensions.  The character fonts available
are vector fonts, so the Bresenham algorithm is used to draw the
vectors.  The fonts have fill vectors so that the characters will appear
solid if plotted at standard size.  When plotted in 3-D the characters
are transformed by the current transformation.	However, since characters
are defined in world coordinates, their position is set by **mov3$abs**
and their orientation in world coordinates is specified as described
below.


```

char$font(font)			set character font:
				bookface, script, greek, Old English
char$size(size)			set character size
char$color(color)		set character color
char$space(dx, dy, dz)		direction in world coordinates for
				character string to proceed
char$up(dx, dy, dz)		up direction of characters in world
				coordinates
text("ascii string")		write text in 3-D
text2("ascii string")		write text in 2-D
mark2(symbol)			draw symbol in 2-D
stext2("ascii string")		simple stick figure text

```


**Transform routines**

These routines maintain the transformation stack, viewport attributes,
and patch template.  Included are routines for concatenating matrices,
transforming points, taking vector crossproducts, computing unit
vectors, obtaining the length of a vector, finding vector dotproducts
and popping and pushing transformations on the transform stack.


```

push(m) float *m;		push 4x4 matrix onto stack
pop(m)	float *m;		pop 4x4 matrix from stack
matcon()			concatenate top matrix times next
				matrix, pop both, push the result on
				the stack
tranpt(p1, p2)			transform point using stack top,
				p2 gets transformed point
crossprod(p1, p2, p3)		vector cross product: p3 = p1 x p2
float dotprod(p1, p2)		vector dot product
unitvec(p1)			convert vector to unit vector
float vecleng(x, y, z)		return length of vector
vw$ref$pt(x, y, z)		set look at point in world coordinates
vwp$norm(dx, dy, dz)		set view plane normal
vwp$dist(vw$dist)		set view distance
vw$up$3(dxup, dyup, dzup)	set upward direction for viewing window
vwindow(umin, umax, vmin, vmax)
				set view window size in world
				coordinates
vw$port$2(xmin, xmax, ymin, ymax)
				set view port in display coordinates
vw$depth(front$dist, back$dist) set near and far clipping planes
vw$parallel(dx, dy, dz)		specify no perspective scaling;
				set direction of projection
vw$perspect(dx, dy, dz)		specify perspective scaling;
				set center of projection
make$mat			build transform from view attributes
				and push it on the stack
clip$vec(p1, p2)		clip vector to window, return true
				if visible

```
