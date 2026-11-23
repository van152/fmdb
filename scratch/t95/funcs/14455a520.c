char __fastcall sub_14455A520(__int64 a1, __int64 a2)
{
  __int64 v3; // rcx
  __int64 v4; // rax
  __int64 v6; // [rsp+28h] [rbp-18h] BYREF
  int v7; // [rsp+30h] [rbp-10h]
  __int64 v8; // [rsp+38h] [rbp-8h]

  v8 = -2;
  v7 = 1095200353;
  v6 = sub_14083D4F0(a1) + 56;
  sub_14083B5F0(a2, &v6);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v6 + 16LL))(v6, &v6);
  v4 = sub_14083D4F0(v3);
  v7 = 1095201646;
  v6 = v4 + 56;
  sub_14083B5F0(a2, &v6);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v6 + 16LL))(v6, &v6);
  return 1;
}
