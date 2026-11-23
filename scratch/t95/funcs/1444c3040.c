__int64 __fastcall sub_1444C3040(__int64 a1, int a2, __int64 *a3)
{
  int v4; // edi
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rcx
  int v8; // edi
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v12; // [rsp+28h] [rbp-18h] BYREF
  __int64 v13; // [rsp+30h] [rbp-10h]
  __int64 v14; // [rsp+38h] [rbp-8h]

  v14 = -2;
  if ( a2 == 1130722425 )
  {
    v8 = *(unsigned __int16 *)(a1 + 32);
    v5 = sub_14083D4F0(a1) + 40;
    LODWORD(v13) = v8;
    v12 = v5;
    if ( &v12 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v9 = v12;
      v10 = v13;
      a3[1] = v13;
      *a3 = v9;
      v5 = sub_14083D4F0(v10) + 8;
      v13 = 0;
      v12 = v5;
    }
    goto LABEL_8;
  }
  if ( a2 == 1130722401 )
  {
    v4 = *(_DWORD *)(a1 + 28);
    v5 = sub_14083D4F0(a1) + 40;
    LODWORD(v13) = v4;
    v12 = v5;
    if ( &v12 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v6 = v12;
      v7 = v13;
      a3[1] = v13;
      *a3 = v6;
      v5 = sub_14083D4F0(v7) + 8;
      v13 = 0;
      v12 = v5;
    }
LABEL_8:
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v5 + 16LL))(v5, &v12);
  }
  return 0;
}
