char __fastcall sub_1444BA710(char *a1, char a2)
{
  bool v2; // zf
  char v3; // cl
  char result; // al

  v2 = a1[1] == 0;
  v3 = *a1;
  if ( v2 || a2 != 0 )
  {
    result = 20;
    if ( v3 <= 19 )
    {
      result = 19;
      if ( v3 <= 17 )
      {
        result = 18;
        if ( v3 <= 15 )
        {
          result = 17;
          if ( v3 <= 13 )
          {
            result = 16;
            if ( v3 <= 11 )
            {
              result = 15;
              if ( v3 <= 9 )
              {
                result = 14;
                if ( v3 <= 7 )
                {
                  result = 13;
                  if ( v3 <= 5 )
                  {
                    result = 12;
                    if ( v3 <= 3 )
                    {
                      result = -1;
                      if ( v3 > 0 )
                        return 11;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  else
  {
    result = 10;
    if ( v3 <= 19 )
    {
      result = 9;
      if ( v3 <= 17 )
      {
        result = 8;
        if ( v3 <= 15 )
        {
          result = 7;
          if ( v3 <= 13 )
          {
            result = 6;
            if ( v3 <= 11 )
            {
              result = 5;
              if ( v3 <= 9 )
              {
                result = 4;
                if ( v3 <= 7 )
                {
                  result = 3;
                  if ( v3 <= 5 )
                  {
                    result = 2;
                    if ( v3 <= 3 )
                      return 2 * (v3 > 0) - 1;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return result;
}
