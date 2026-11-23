__int64 __fastcall sub_143686540(__int64 a1, unsigned int a2)
{
  unsigned int v4; // esi
  _QWORD v6[5]; // [rsp+28h] [rbp-18h] BYREF

  v6[2] = -2;
  v6[1] = 0;
  v6[0] = sub_14083D4F0(a1) + 8;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, _QWORD *))(*(_QWORD *)a1 + 16LL))(a1, a2, v6) != 0 )
    v4 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v6[0] + 48LL))(v6[0], v6);
  else
    v4 = 0;
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v6[0] + 16LL))(v6[0], v6);
  return v4;
}
