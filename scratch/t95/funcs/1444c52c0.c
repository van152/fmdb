char __fastcall sub_1444C52C0(__int64 a1, int a2, __int64 *a3)
{
  char result; // al
  int v5; // edi
  __int64 v6; // rax
  __int64 v7; // rax
  __int64 v8; // rcx
  int v9; // xmm6_4
  __int64 v10; // rax
  __int64 v11; // rcx
  int v12; // edi
  __int64 v13; // rax
  __int64 v14; // rcx
  char v15; // bl
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // [rsp+28h] [rbp-28h] BYREF
  __int64 v19; // [rsp+30h] [rbp-20h]
  __int64 v20; // [rsp+38h] [rbp-18h]

  v20 = -2;
  result = 0;
  if ( a2 > 1768386158 )
  {
    if ( a2 == 1768386159 )
    {
      v15 = *(_BYTE *)(a1 + 36);
      v6 = sub_14083D4F0(a1) + 24;
      LOBYTE(v19) = v15;
      v18 = v6;
      if ( &v18 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v16 = v18;
        v17 = v19;
        a3[1] = v19;
        *a3 = v16;
        v6 = sub_14083D4F0(v17) + 8;
        v19 = 0;
        v18 = v6;
      }
    }
    else
    {
      if ( a2 != 1885696611 )
        return result;
      v9 = *(_DWORD *)(a1 + 32);
      v6 = sub_14083D4F0(a1) + 104;
      LODWORD(v19) = v9;
      v18 = v6;
      if ( &v18 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v10 = v18;
        v11 = v19;
        a3[1] = v19;
        *a3 = v10;
        v6 = sub_14083D4F0(v11) + 8;
        v19 = 0;
        v18 = v6;
      }
    }
  }
  else if ( a2 == 1181639028 )
  {
    v12 = *(_DWORD *)(a1 + 24);
    v6 = sub_14083D4F0(a1) + 40;
    LODWORD(v19) = v12;
    v18 = v6;
    if ( &v18 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v13 = v18;
      v14 = v19;
      a3[1] = v19;
      *a3 = v13;
      v6 = sub_14083D4F0(v14) + 8;
      v19 = 0;
      v18 = v6;
    }
  }
  else
  {
    if ( a2 != 1399742836 )
      return result;
    v5 = *(_DWORD *)(a1 + 28);
    v6 = sub_14083D4F0(a1) + 40;
    LODWORD(v19) = v5;
    v18 = v6;
    if ( &v18 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v7 = v18;
      v8 = v19;
      a3[1] = v19;
      *a3 = v7;
      v6 = sub_14083D4F0(v8) + 8;
      v19 = 0;
      v18 = v6;
    }
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v6 + 16LL))(v6, &v18);
  return 1;
}
