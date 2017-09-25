C file: FIB1.F90
      subroutine FIB(i, j, t1, t2, f1, f2, t, i2, j2, check)
C
C     Compare values, if t1 is greater than t2, t2 gets written
C	  to t, j increases 1, i stays the same. In every other case,
C	  if t2 is greater than t1 OR if t1==t2, t1 gets written to t.
C
	  implicit none
C
      integer i, j, f1, f2, i2, j2, check
	  integer(kind=8) t1, t2, t
	  intent(in) i, j, t1, t2, f1, f2
	  intent(out) i2, j2, check, t
C		
	  if (t1.gt.t2) then
        t=t2
        j2=j+1
		i2=i
      else
        t=t1
        i2=i+1
		j2=j
	  endif
	  check=1
	  if ((i2.eq.f1).or.(j2.eq.f2)) then
        check=0
	  endif
      end subroutine
C end file FIB1.F90