__int64 __fastcall sub_143E5AB90(__int64 a1, __int64 *a2)
{
  _QWORD *v3; // rdi
  _QWORD v6[6]; // [rsp+20h] [rbp-10h] BYREF

  v6[2] = -2;
  v3 = *(_QWORD **)(a1 + 48);
  if ( v3 == nullptr )
  {
    v3 = (_QWORD *)sub_14007A910(24);
    sub_1407C9510(v3);
    *(_QWORD *)(a1 + 48) = v3;
  }
  sub_14083DDA0(v6, a2);
  sub_14083B5F0(v3, v6);
  return (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v6[0] + 16LL))(v6[0], v6);
}
