__int64 __fastcall sub_143EE6D10(__int64 a1, char a2, __int64 a3, int a4, unsigned __int8 a5)
{
  unsigned int v5; // ebp
  int v7; // esi
  int v8; // edi
  int v9; // edx

  if ( a2 == 0 )
    goto LABEL_6;
  v7 = a3;
  v8 = a1;
  v9 = a1 + 48;
  if ( *(_BYTE *)(a1 + 47) != 0 )
    sub_140F7EC80(a3, v9, *(_QWORD *)(a3 + 96), a5, 1, 0);
  else
    sub_140F7EE40(a3, v9, *(_QWORD *)(a3 + 16), a5, 1, 0);
  v5 = 0;
  if ( (unsigned __int8)sub_1411A1640(v8, 0, v7, a4, a5) != 0 )
LABEL_6:
    LOBYTE(v5) = 1;
  return v5;
}
