__int64 __fastcall sub_143ADC280(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rdi
  int v5; // r9d
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v7; // rcx
  unsigned int v8; // esi
  void (__fastcall ***v9)(_QWORD, __int64); // rcx
  __int64 v11; // [rsp+28h] [rbp-28h] BYREF
  char v12[8]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v13; // [rsp+38h] [rbp-18h] BYREF
  __int64 v14; // [rsp+40h] [rbp-10h] BYREF
  _QWORD v15[5]; // [rsp+48h] [rbp-8h] BYREF

  v15[1] = -2;
  sub_14080D0E0(a1: v12, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 7);
  *(_QWORD *)v4 = 0x700000000LL;
  *(_DWORD *)(v4 + 8) = MEMORY[0x1418FF924];
  *(_DWORD *)(v4 + 11) = MEMORY[0x1418FF927];
  *(_BYTE *)(v4 + 15) = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v13 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v13 = v4 + 4;
  v11 = 0x80100004E554C4CLL;
  if ( *a2 != 0
    && ((*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, char *))(*(_QWORD *)*a2 + 224LL))(
          a1: *a2,
          a2: &v14,
          a3: &v13,
          a4: v12),
        v14 != 0) )
  {
    LOWORD(v5) = 3;
    sub_1407D1280(a1: (unsigned int)&v11, a2: (unsigned int)v15, a3: (unsigned int)&v14, a4: v5, a5: 0);
    v6 = (void (__fastcall ***)(_QWORD, __int64))v14;
    if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
      (**v6)(a1: v6, a2: 1);
  }
  else
  {
    v15[0] = 0;
  }
  v7 = v13;
  if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 - 4)) == 0 )
    sub_1412EC9A0(a1: v7 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  if ( v15[0] != 0 )
  {
    v8 = (*(__int64 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)a1 + 64LL))(a1, a2: v15);
    v9 = (void (__fastcall ***)(_QWORD, __int64))v15[0];
    if ( v15[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15[0] + 8LL)) == 0 )
      (**v9)(a1: v9, a2: 1);
  }
  else
  {
    return 0;
  }
  return v8;
}
