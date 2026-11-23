__int64 __fastcall sub_140F5C7E0(int a1)
{
  unsigned __int64 v1; // rax
  __int64 *v2; // rdx
  __int64 v3; // rcx
  __int64 v4; // rdx

  if ( a1 < 0 )
    return 0;
  v1 = (unsigned int)a1;
  if ( (_BYTE)word_141B60320 != 0 )
  {
    v2 = *(__int64 **)(qword_141B5FE40 + 128);
    v3 = *v2;
    v4 = v2[1];
  }
  else
  {
    v3 = *(_QWORD *)(qword_141B5FE40 + 96);
    v4 = *(_QWORD *)(qword_141B5FE40 + 104);
  }
  if ( (v4 - v3) >> 3 <= v1 )
    return 0;
  else
    return *(_QWORD *)(v3 + 8 * v1);
}
