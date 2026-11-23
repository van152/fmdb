int *__fastcall sub_143C8A630(int *a1, _QWORD *a2, unsigned __int8 *a3)
{
  int v6; // ecx
  unsigned __int64 v7; // rsi
  unsigned __int8 v8; // al
  unsigned __int64 v9; // rax
  __int16 v11; // [rsp+22h] [rbp-36h] BYREF
  _DWORD v12[13]; // [rsp+24h] [rbp-34h] BYREF

  v12[0] = 0;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v12, a3: 4);
  v6 = 1;
  if ( qword_141AA7808 > (unsigned __int64)v12[0] )
  {
    if ( v12[0] != 0 )
    {
      v7 = 0;
      do
      {
        v11 = 0;
        (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v11, a3: 2);
        if ( *(_DWORD *)(*a2 + 16LL) != 0 )
          break;
        v9 = *a3;
        if ( v9 > 5 )
        {
          *(_WORD *)&a3[2 * a3[14] + 2] = v11;
          v8 = a3[14] + 1;
          if ( v8 >= 6u )
            v8 = 0;
          a3[14] = v8;
        }
        else
        {
          *(_WORD *)&a3[2 * v9 + 2] = v11;
          *a3 = v9 + 1;
        }
        ++v7;
      }
      while ( v7 < v12[0] );
    }
    v6 = *(_DWORD *)(*a2 + 16LL);
  }
  *a1 = v6;
  return a1;
}
