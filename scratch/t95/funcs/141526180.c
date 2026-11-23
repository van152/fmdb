// THUNK ALIAS -> sub_1444B84C0 (jmp:0x141526180->0x1444b84c0)
char __fastcall sub_1444B84C0(char *a1)
{
  bool v1; // zf
  char v2; // cl
  char result; // al

  v1 = a1[1] == 0;
  v2 = *a1;
  if ( v1 )
  {
    result = 20;
    if ( v2 <= 19 )
    {
      result = 19;
      if ( v2 <= 17 )
      {
        result = 18;
        if ( v2 <= 15 )
        {
          result = 17;
          if ( v2 <= 13 )
          {
            result = 16;
            if ( v2 <= 11 )
            {
              result = 15;
              if ( v2 <= 9 )
              {
                result = 14;
                if ( v2 <= 7 )
                {
                  result = 13;
                  if ( v2 <= 5 )
                  {
                    result = 12;
                    if ( v2 <= 3 )
                    {
                      result = -1;
                      if ( v2 > 0 )
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
    if ( v2 <= 19 )
    {
      result = 9;
      if ( v2 <= 17 )
      {
        result = 8;
        if ( v2 <= 15 )
        {
          result = 7;
          if ( v2 <= 13 )
          {
            result = 6;
            if ( v2 <= 11 )
            {
              result = 5;
              if ( v2 <= 9 )
              {
                result = 4;
                if ( v2 <= 7 )
                {
                  result = 3;
                  if ( v2 <= 5 )
                  {
                    result = 2;
                    if ( v2 <= 3 )
                      return 2 * (v2 > 0) - 1;
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
