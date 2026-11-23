__int64 __fastcall sub_141530440(__int64 a1, int a2, __int64 *a3)
{
  __int64 v4; // rdi
  int v5; // edi
  __int64 v6; // rax
  __int64 v7; // rax
  __int64 v8; // rcx
  int v9; // edi
  __int64 v10; // rax
  __int64 v11; // rcx
  int v12; // edi
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rax
  __int64 v16; // rcx
  __int64 v18; // [rsp+28h] [rbp-18h] BYREF
  __int64 v19; // [rsp+30h] [rbp-10h]
  __int64 v20; // [rsp+38h] [rbp-8h]

  v20 = -2;
  LODWORD(v4) = 0;
  if ( a2 > 1851880552 )
  {
    if ( a2 == 1918989417 )
    {
      LODWORD(v4) = *(char *)(a1 + 32);
      if ( *(_BYTE *)(a1 + 32) != 0 )
      {
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v19) = v4;
        v18 = v6;
        if ( &v18 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v15 = v18;
          v16 = v19;
          a3[1] = v19;
          *a3 = v15;
          v6 = sub_14083D4F0(v16) + 8;
          v19 = 0;
          v18 = v6;
        }
        goto LABEL_18;
      }
      LOBYTE(v4) = 1;
      if ( a3 != &qword_141B5A4A0 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          a3);
      }
    }
    else if ( a2 == 1851880553 )
    {
      v9 = *(_DWORD *)(a1 + 28);
      v6 = sub_14083D4F0(a1) + 40;
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
      goto LABEL_18;
    }
  }
  else
  {
    if ( a2 == 1835104353 )
    {
      v12 = *(unsigned __int8 *)(a1 + 34);
      v6 = sub_14083D4F0(a1) + 56;
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
      goto LABEL_18;
    }
    if ( a2 == 1835626081 )
    {
      v5 = *(unsigned __int8 *)(a1 + 33);
      v6 = sub_14083D4F0(a1) + 56;
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
LABEL_18:
      v4 = *(_QWORD *)v6;
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v6 + 16LL))(v6, &v18);
      LOBYTE(v4) = 1;
    }
  }
  return (unsigned int)v4;
}
