__int64 __fastcall sub_143CDF010(__int64 a1, __int64 *a2)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  __int64 v6; // rax
  __int64 v7; // rcx
  int v9; // [rsp+28h] [rbp-38h] BYREF
  _QWORD v10[2]; // [rsp+30h] [rbp-30h] BYREF
  __int64 v11; // [rsp+40h] [rbp-20h] BYREF
  __int64 v12; // [rsp+48h] [rbp-18h] BYREF
  __int64 v13; // [rsp+50h] [rbp-10h]
  __int64 v14; // [rsp+58h] [rbp-8h]

  v14 = -2;
  v12 = 0;
  v11 = sub_14083D4F0(a1) + 8;
  (*(void (__fastcall **)(__int64, __int64 *, _QWORD *))(*(_QWORD *)v11 + 24LL))(v11, &v11, v10);
  v9 = -8388609;
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v11 + 16LL))(v11, &v11);
  if ( a1 != 0 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)a1 + 144LL))(a1, &v11);
    v9 = v11;
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v10[0] + 16LL))(v10[0], v10);
    v10[1] = v13;
    v10[0] = v12;
    v4 = sub_14083D4F0(v13);
    v13 = 0;
    v12 = v4 + 8;
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)(v4 + 8) + 16LL))(v4 + 8, &v12);
  }
  sub_140FEAD00(&v9, &v11);
  v5 = *a2;
  if ( &v11 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v5 + 16LL))(v5, a2);
    v6 = v11;
    v7 = v12;
    a2[1] = v12;
    *a2 = v6;
    v5 = sub_14083D4F0(v7) + 8;
    v12 = 0;
    v11 = v5;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v5 + 16LL))(v5, &v11);
  return (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v10[0] + 16LL))(v10[0], v10);
}
