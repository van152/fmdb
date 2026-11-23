char __fastcall sub_144551D10(__int64 a1, int a2, __int64 *a3)
{
  __int64 *v4; // rdi
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 *v10; // rdi
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rax
  __int64 v14; // rcx
  char v15; // bl
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 *v18; // rdi
  __int64 v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v24; // [rsp+20h] [rbp-10h] BYREF
  _QWORD v25[5]; // [rsp+28h] [rbp-8h] BYREF

  v25[1] = -2;
  if ( a2 > 1397649517 )
  {
    if ( a2 == 1397649518 )
    {
      v18 = (__int64 *)(a1 + 40);
      v19 = sub_14083D4F0(a1);
      v25[0] = 0;
      if ( v25 != v18 )
      {
        v20 = *v18;
        if ( *v18 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v20 - 4));
        v25[0] = v20;
      }
      v7 = v19 + 136;
      v24 = v7;
      if ( &v24 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v21 = v24;
        v22 = v25[0];
        a3[1] = v25[0];
        *a3 = v21;
        v7 = sub_14083D4F0(v22) + 8;
        v25[0] = 0;
        v24 = v7;
      }
      goto LABEL_29;
    }
    if ( a2 == 1397650286 )
    {
      v10 = (__int64 *)(a1 + 32);
      v11 = sub_14083D4F0(a1);
      v25[0] = 0;
      if ( v25 != v10 )
      {
        v12 = *v10;
        if ( *v10 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v12 - 4));
        v25[0] = v12;
      }
      v7 = v11 + 136;
      v24 = v7;
      if ( &v24 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v13 = v24;
        v14 = v25[0];
        a3[1] = v25[0];
        *a3 = v13;
        v7 = sub_14083D4F0(v14) + 8;
        v25[0] = 0;
        v24 = v7;
      }
      goto LABEL_29;
    }
  }
  else
  {
    if ( a2 == 1145392197 )
    {
      v15 = *(_BYTE *)(a1 + 59);
      v7 = sub_14083D4F0(a1) + 24;
      LOBYTE(v25[0]) = (v15 & 2) != 0;
      v24 = v7;
      if ( &v24 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v16 = v24;
        v17 = v25[0];
        a3[1] = v25[0];
        *a3 = v16;
        v7 = sub_14083D4F0(v17) + 8;
        v25[0] = 0;
        v24 = v7;
      }
      goto LABEL_29;
    }
    if ( a2 == 1397648993 )
    {
      v4 = (__int64 *)(a1 + 24);
      v5 = sub_14083D4F0(a1);
      v25[0] = 0;
      if ( v25 != v4 )
      {
        v6 = *v4;
        if ( *v4 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v6 - 4));
        v25[0] = v6;
      }
      v7 = v5 + 136;
      v24 = v7;
      if ( &v24 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v8 = v24;
        v9 = v25[0];
        a3[1] = v25[0];
        *a3 = v8;
        v7 = sub_14083D4F0(v9) + 8;
        v25[0] = 0;
        v24 = v7;
      }
LABEL_29:
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v7 + 16LL))(v7, &v24);
      return 1;
    }
  }
  return sub_140FE3F20((_DWORD *)a1, a2, a3);
}
