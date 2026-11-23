__int64 __fastcall sub_141191E80(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  __int64 result; // rax
  _DWORD *v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx

  v4 = (_DWORD *)*a2;
  result = (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(v4, a1 + 8, 4);
  if ( v4[4] == 0 )
  {
    v6 = (_DWORD *)*a2;
    result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
    if ( v6[4] == 0 )
    {
      v7 = *a2;
      result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 20, 4);
      if ( *(_DWORD *)(v7 + 16) == 0 )
      {
        v8 = *a2;
        result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
        if ( *(_DWORD *)(v8 + 16) == 0 )
        {
          v9 = *a2;
          result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 16, 4);
          if ( *(_DWORD *)(v9 + 16) == 0 )
          {
            v10 = *a2;
            result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 28, 4);
            if ( *(_DWORD *)(v10 + 16) == 0 )
            {
              result = sub_140DB8980(a1 + 32, a2);
              if ( (_BYTE)result != 0 )
              {
                result = sub_140DB8980(a1 + 36, a2);
                if ( (_BYTE)result != 0 )
                {
                  v11 = *a2;
                  result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                             *a2,
                             a1 + 40,
                             1);
                  if ( *(_DWORD *)(v11 + 16) == 0 )
                  {
                    v12 = *a2;
                    result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1, 4);
                    if ( *(_DWORD *)(v12 + 16) == 0 )
                      return (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                               *a2,
                               a1 + 41,
                               1);
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
