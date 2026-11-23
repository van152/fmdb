__int64 __fastcall sub_14447E770(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 result; // rax
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  char v9; // cl
  _DWORD *v10; // rdi
  char v11; // cl
  char v12; // [rsp+2Eh] [rbp-1Ah] BYREF
  _BYTE v13[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  result = (*(__int64 (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v13, a3: 1);
  if ( *(_DWORD *)(v4 + 16) == 0 )
  {
    v6 = *a2;
    result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 2);
    if ( *(_DWORD *)(v6 + 16) == 0 )
    {
      v7 = *a2;
      result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 2, a3: 1);
      if ( *(_DWORD *)(v7 + 16) == 0 )
      {
        v12 = 0;
        v8 = *a2;
        result = (*(__int64 (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v12, a3: 1);
        if ( *(_DWORD *)(v8 + 16) == 0 )
        {
          v9 = 30;
          if ( (unsigned __int8)v12 < 0x1Eu )
            v9 = v12;
          *(_BYTE *)(a1 + 3) = v9 | *(_BYTE *)(a1 + 3) & 0xC0;
          v10 = (_DWORD *)*a2;
          result = (*(__int64 (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v10 + 40LL))(
                     a1: v10,
                     a2: &v12,
                     a3: 1);
          if ( v10[4] == 0 )
          {
            v11 = 3;
            if ( (unsigned __int8)v12 < 3u )
              v11 = v12;
            result = *(unsigned __int8 *)(a1 + 3);
            LOBYTE(result) = (v11 << 6) | result & 0x3F;
            *(_BYTE *)(a1 + 3) = result;
          }
        }
      }
    }
  }
  return result;
}
